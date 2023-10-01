# -*- coding: utf-8 -*-

import importlib
import streamlit as st
from typer import Typer, run, Exit
from click import option
from typing import List

from cookiecutter.main import cookiecutter

app = Typer()

@app.command()
def main(
    template: str = option(
        "-t",
        "--template",
        help="The Cookiecutter template to use.",
        required=True,
    ),
    extra_context: List[str] = option(
        "-e",
        "--extra-context",
        help="Extra context to pass to the Cookiecutter template.",
        multiple=True,
    ),
):
    """Create a project from a Cookiecutter project template."""

    # Create a Cookiecutter context from the user's input.
    extra_context = dict(extra_context or [])
    context = cookiecutter.Context(
        template=template,
        extra_context=extra_context,
    )
    
    # Generate the project.
    # cookiecutter.generate_files(
    #     repo_dir=".", context=context, overwrite_if_exists=True
    # )
    cookiecutter(template=context.template, no_input=True, extra_context=context.extra_context)
    
    # Import the generate module.
    module_name = f"{context['repo_name']}.{context['repo_name']}"
    module = importlib.import_module(module_name)
    
    # Call the module's main function.
    module.main()
    
    # Create a Streamlit form to collect the user's input.
    with st.form("cookiecutter_form"):
        st.text_input("Template", template)
        extra_context_form = st.form_submit_button("Generate")

    # If the user submits the form, generate the project.
    if extra_context_form:
        try:
            cookiecutter(template, extra_context=extra_context)
        except Exception as e:
            st.error(e)
            raise Exit(1)

    # Display a success message to the user.
    st.success("Project generated successfully!")

# if __name__ == "__main__":
#     run(main)