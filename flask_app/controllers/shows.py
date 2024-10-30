from flask_app import app, bcrypt
from flask_app.models.show import Show
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.get("/shows/all")
def all_shows():
    """This route renders all shows"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    shows = Show.find_all_with_users()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_shows.html", shows=shows, user=user)


@app.get("/shows/new")
def new_show():
    """This route displays the new show form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("new_show.html", user=user)


@app.post("/shows/create")
def create_shows():
    """This route processes the new show form."""

    if not Show.form_is_valid(request.form):
        return redirect("/shows/new")

    # down here the form is valid!!
    Show.create(request.form)
    return redirect("/shows/all")


@app.get("/shows/dashboard")
def shows_dashboard():
    """This route displays the user dashboard."""
    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])

    return render_template("dashboard.html", user=user)


@app.get("/shows/<int:show_id>")
def shows_id(show_id):
    """This route displays one users shows details"""

    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    show = Show.find_by_user_id(show_id)
    user = User.find_by_user_id(session["user_id"])

    return render_template("show_program.html", user=user, show=show)


@app.get("/shows/<int:show_id>/edit")
def edit_show(show_id):
    """This route displays the edit show form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    show = Show.find_by_user_id(show_id)
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_show.html", show=show, user=user)


@app.post("/shows/update")
def update_show():
    """This route displays the edit show form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    show_id = request.form["show_id"]

    if not Show.form_is_valid(request.form):
        return redirect(f"/shows/{show_id}/edit")

    # down here the form is valid
    Show.update(request.form)
    return redirect(f"/shows/{show_id}")


@app.get("/shows/<int:show_id>/delete")
def delete_show(show_id):
    """This route processes the delete form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    Show.delete(show_id)
    return redirect("/shows/all")
