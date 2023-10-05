"""Project sub command cli."""
import io
import os
import sys
import tempfile
import time
from pathlib import Path

import click
import rich
import rich.console
import rich.json
from PIL import Image

import ikcli.utils.rich
from ikcli.common.cli import role_choice, visibility_choice
from ikcli.namespaces.core import Namespaces
from ikcli.users.core import Users

from .core import Projects

# Click choice on cloud providers
provider_choice = click.Choice(["AWS", "SCALEWAY_VIA_SCALEDYNAMICS"], case_sensitive=False)

# Click choice on cloud provider region
provider_region_choice = click.Choice(["FRANCE", "GERMANY", "IRELAND"], case_sensitive=False)

# Click choice on deployment flavour
provider_flavour_choice = click.Choice(["SERVERLESS", "CLUSTER", "GPU"], case_sensitive=False)

# Click choice on deployment size
provider_size_choice = click.Choice(["S", "M", "L", "XL"], case_sensitive=False)

# A decorator to give Projects object to commands
pass_projects = click.make_pass_decorator(Projects)


@click.group(name="project")
@click.pass_context
def cli_project(ctx):
    """Manage projects."""
    ctx.obj = Projects(ctx.obj)


@cli_project.command(name="ls")
@click.option("--name", help="Filter projects by name")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_projects
def cli_project_list(projects, name, limit):
    """List projects."""
    ikcli.utils.rich.table(
        projects.list(name=name).limit(limit),
        "Projects",
        ["name", "path", "description", "visibility"],
    )


@cli_project.command(name="add")
@click.option("--description", help="Project description")
@click.option("--visibility", type=visibility_choice, help="Project visibility")
@click.argument("namespace")
@click.argument("name")
@pass_projects
def cli_project_add(projects, namespace, name, description, visibility):
    """Add project NAME on NAMESPACE."""
    # Get namespace
    namespace = Namespaces(projects.get_http_request()).get(name=namespace)

    # Add project
    ikcli.utils.rich.create(
        f"Add Project '{name}' to {namespace}",
        namespace.projects,
        name=name,
        description=description,
        visibility=visibility,
    )


@cli_project.command(name="show")
@click.argument("name")
@pass_projects
def cli_project_show(projects, name):
    """Show project NAME."""
    try:
        project = projects.get(name=name)
    except ikcli.net.api.exceptions.ObjectNotFoundException:
        rich.print(f"[orange3]Unable to find project {name}.")
        sys.exit(1)

    # Get member list
    members = project.members.list()
    extra = [ikcli.utils.rich.table(members, "Members", ["username", "role", "source"], display=False)]

    # Display project
    ikcli.utils.rich.show(project, "Project", ["name", "description", "visibility"], extra=extra)


@cli_project.command(name="delete")
@click.argument("name")
@pass_projects
def cli_project_delete(projects, name):
    """Delete project NAME."""
    ikcli.utils.rich.delete(projects.get(name=name))


@cli_project.command(name="push")
@click.argument("name")
@click.argument(
    "workflow_filename",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, path_type=Path),
)
@pass_projects
def cli_project_push(projects, name, workflow_filename):
    """
    Push workflow to project.

    NAME                Project name.
    WORKFLOW_FILENAME   Path to workflow json file.
    """
    # Get project
    project = projects.get(name=name)

    # Push workflow
    console = rich.console.Console()
    with ikcli.utils.rich.HTTPTransferProgress("Workflow", project.get_http_request(), download=False, upload=True):
        workflow = project.workflows.create(workflow_filename)
    console.print(f"[green] {workflow}")


#
#   Members
#
@cli_project.group(name="member")
def cli_project_member():
    """Manage project members."""
    pass


@cli_project_member.command(name="ls")
@click.argument("project_name")
@click.option("--username", help="Filter project members by name")
@click.option("--role", type=role_choice, help="Filter project members by role")
@pass_projects
def cli_project_member_list(projects, project_name, username, role):
    """List project members."""
    # Get project and members
    project = projects.get(name=project_name)
    members = project.members.list(username=username, role=role)

    # Display on table
    ikcli.utils.rich.table(members, "Members", ["username", "role", "source"])


@cli_project_member.command(name="add")
@click.argument("project_name")
@click.argument("username")
@click.argument("role", type=role_choice)
@pass_projects
def cli_project_member_add(projects, project_name, username, role):
    """Add project members."""
    # Get project and user
    project = projects.get(name=project_name)
    user = Users(projects.get_http_request()).get(username=username)
    ikcli.utils.rich.create(
        f"Add '{username}' as {project_name}'s {role}",
        project.members,
        user=user,
        role=role,
    )


@cli_project_member.command(name="delete")
@click.argument("project_name")
@click.argument("username")
@pass_projects
def cli_project_member_delete(projects, project_name, username):
    """Remove project member."""
    # Get project and member
    project = projects.get(name=project_name)
    member = project.members.get(username=username)
    ikcli.utils.rich.delete(member)


#
#   Workflow
#
@cli_project.group(name="workflow")
def cli_workflow():
    """Manage workflows."""
    pass


@cli_workflow.command(name="ls")
@click.argument("project_name")
@click.option("--name", help="Filter workflow by name")
@click.option("--limit", type=int, default=20, help="Specify how many rows to display")
@pass_projects
def cli_workflow_list(projects, project_name, name, limit):
    """List workflows."""
    # Get project
    project = projects.get(name=project_name)

    # Display workflow
    ikcli.utils.rich.table(
        project.workflows.list(name=name).limit(limit),
        "Workflows",
        ["name", "description", "tag"],
    )


@cli_workflow.command(name="show")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_workflow_show(projects, project_name, workflow_name):
    """Show workflow."""
    # Get project
    project = projects.get(name=project_name)

    # Get workflow
    workflow = project.workflows.get(name=workflow_name)
    rich.print_json(data=workflow["data"])


@cli_workflow.command(name="deploy")
@click.argument("project_name")
@click.argument("workflow_name")
@click.argument("provider", type=provider_choice)
@click.argument("region", type=provider_region_choice)
@click.argument("flavour", type=provider_flavour_choice)
@click.option("--size", type=provider_size_choice, default="M")
@pass_projects
def cli_workflow_deploy(projects, project_name, workflow_name, provider, region, flavour, size):
    """Deploy workflow."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Create deployment
    console = rich.console.Console()
    with console.status(f"[cyan]Deploying {workflow} to {provider} {flavour} {region} ...", spinner="earth"):
        deployment = workflow.deployments.create(provider=provider, flavour=flavour, region=region, size=size)
    console.print(f"\U0001F30D  [bold green]{deployment}")


@cli_workflow.command(name="delete")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_workflow_delete(projects, project_name, workflow_name):
    """Delete workflow."""
    # Get project
    project = projects.get(name=project_name)

    # Delete workflow
    ikcli.utils.rich.delete(project.workflows.get(name=workflow_name))


#
#   Deployment
#
@cli_project.group(name="deployment")
def cli_deployment():
    """Manage deployments."""
    pass


@cli_deployment.command(name="ls")
@click.argument("project_name")
@click.argument("workflow_name")
@pass_projects
def cli_deployment_list(projects, project_name, workflow_name):
    """List deployments."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # List deployments
    ikcli.utils.rich.table(
        workflow.deployments.list(),
        "Deployments",
        ["provider", "region", "flavour", "size", "tag", "status", "endpoint"],
    )


@cli_deployment.command(name="update")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option("--size", type=provider_size_choice, default=None)
@pass_projects
def cli_deployment_update(projects, project_name, workflow_name, provider, region, flavour, size):
    """Update deployment against workflow or size."""
    console = rich.console.Console()

    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Get deployments to update
    deployments = [
        deployment
        for deployment in workflow.deployments.list(provider=provider, region=region, flavour=flavour)
        if (deployment["tag"] != workflow["tag"])
        or (size is not None and deployment["size"] != size)
        or deployment["status"] == "ERROR"
    ]
    if len(deployments) == 0:
        console.print("[orange3]Nothing to update")
        return

    # Display and confirm
    ikcli.utils.rich.table(
        deployments,
        "Will update these deployments",
        ["provider", "region", "flavour", "size", "tag", "status", "endpoint"],
    )

    if not rich.prompt.Confirm.ask("Continue to update ?"):
        console.print("[orange3]Aborted by user")
        return

    # Update each one
    for deployment in deployments:
        with console.status(f"[cyan]Updating {deployment} ..."):
            if size is not None:
                deployment["size"] = size
            deployment.update()
        console.print("[green]Done")


@cli_deployment.command(name="run")
@click.argument("project_name")
@click.argument("workflow_name")
@click.argument(
    "image",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, path_type=Path),
)
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@click.option("--task", help="Workflow task to query. Will prompt user if not given")
@click.option("--output-index", type=click.INT, multiple=True, help="Output index to display (default = all)")
@click.option("--polling", type=click.INT, help="time in seconds between 2 poll when wait for response", default=5)
@pass_projects
def cli_deployment_run(
    projects, project_name, workflow_name, image, provider, region, flavour, task, output_index, polling
):
    """Call deployment endpoint on image."""
    # Get project, workflow and deployment
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)

    # If task wasn't specified, ask to user to choose one
    if task is None:
        task_options = {task["task_data"]["name"]: task["task_data"]["name"] for task in workflow["data"]["tasks"]}
        if len(task_options) == 1:
            task = next(iter(task_options))
        else:
            task = ikcli.utils.rich.menu("Choose a task", task_options)

    # Query endpoint
    console = rich.console.Console()
    with console.status(f"[cyan]Querying {deployment} ..."):
        # Get endpoint HTTPRequest object and query
        start = time.time()
        outputs = list(
            deployment.get_endpoint_http_request().run(task, image, output_indexes=output_index, polling=polling)
        )
        duration = int(time.time() - start)

    # Display outputs
    for counter, output in enumerate(outputs):
        (typ, data) = next(iter(output.items()))
        title = f"{typ} ({counter})" if len(output_index) == 0 else typ

        # If type is image, save it and display
        if typ in ("image", "image_binary"):
            image = Image.open(io.BytesIO(data))
            fd, path = tempfile.mkstemp(
                prefix=f"ikcli - {project_name} - {workflow_name} (", suffix=f") {title}.{image.format}"
            )
            with os.fdopen(fd, "w") as fh:
                image.save(fh, image.format)
            ikcli.utils.rich.show_image(path, title=title)
            data = ["Image saved as", path]

        # All data are displayed as JSON
        rich.print(
            rich.panel.Panel(
                rich.padding.Padding(rich.json.JSON.from_data(data=data), (1, 1)),
                title=title,
                width=80,
                border_style="bold green",
            )
        )

    # Print duration
    console.print(f"[green] Done in {duration} seconds")


@cli_deployment.command(name="delete")
@click.argument("project_name")
@click.argument("workflow_name")
@click.option("--provider", type=provider_choice, help="Cloud provider")
@click.option("--region", type=provider_region_choice, help="Cloud provider region")
@click.option("--flavour", type=provider_flavour_choice, help="Deployment flavour")
@pass_projects
def cli_deployment_delete(projects, project_name, workflow_name, provider, region, flavour):
    """Delete deployments."""
    # Get project and workflow
    project = projects.get(name=project_name)
    workflow = project.workflows.get(name=workflow_name)

    # Get deployment and delete
    deployment = workflow.deployments.get(provider=provider, region=region, flavour=flavour)
    ikcli.utils.rich.delete(deployment)
