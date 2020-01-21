import os
import json

import remi.gui as gui
from remi import App

from PersonalAssistant import PersonalAssistant

TITLE_BOX_STYLES = {
  "font-family": "Montserrat, Arial",
  "text-transform": "uppercase",
  "box-shadow": "none",
  "border": "1px solid #d7d7d7",
}

LABEL_STYLES = {
  "font-family": "Montserrat, Arial",
  "text-transform": "none",
  "margin": "10px 0px 0px 20px",
  "font-size": "16px",
  "color": "#3b3b3b"
}

TEXT_INPUT_STYLES = {
  "padding-top": "10px",
  "padding-left": "10px",
  "margin": "10px 0px 0px 20px",
}


class BaseApp(App):
  def __init__(self, *args, **kwargs):
    res_path = os.path.join(os.path.dirname(__file__), "res")
    super(BaseApp, self).__init__(*args,
                                  **kwargs,
                                  static_file_path={"res": res_path})

  def todo_drop_down_changed(self, widget, value):
    self.clear_errors()
    if value == "Add a to-do":
      self.dialog = gui.GenericDialog(title="＋ Add a to-do",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      self.label = gui.Label("Enter a to-do item: ",
                             width=200,
                             height=30,
                             style=LABEL_STYLES)
      self.textinput = gui.TextInput(width=200,
                                     height=30,
                                     style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.label)
      self.dialog.add_field("label1", self.textinput)
      self.dialog.confirm_dialog.connect(self.add_todo)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Remove a to-do":
      self.dialog = gui.GenericDialog(title="✘ Remove a to-do",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      self.headText = gui.Label("Current to-do items: ",
                                width=200,
                                height=30,
                                style=LABEL_STYLES)
      self.dialog.add_field("label2", self.headText)
      data = self.assistant.get_todo()
      for i in range(len(data)):
        self.dialog.add_field(
          "labels" + str(i),
          gui.Label("- " + data[i], width=200, height=30, style=LABEL_STYLES),
        )
      self.label = gui.Label(
        "Enter item to remove: ",
        width=200,
        height=30,
        style=LABEL_STYLES,
      )
      self.textinput = gui.TextInput(width=200,
                                     height=30,
                                     style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.label)
      self.dialog.add_field("label1", self.textinput)
      self.dialog.confirm_dialog.connect(self.remove_todo)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Get to-do list":
      self.dialog = gui.GenericDialog(width="500px",
                                      title="✔️ To-do list",
                                      style=TITLE_BOX_STYLES)
      self.headText = gui.Label("To-do items: ",
                                width=300,
                                height=30,
                                style=LABEL_STYLES)
      self.dialog.add_field("label", self.headText)
      data = self.assistant.get_todo()
      for i in range(len(data)):
        self.dialog.add_field(
          "label" + str(i),
          gui.Label("- " + data[i], width=200, height=30, style=LABEL_STYLES),
        )
      self.dialog.confirm_dialog.connect(self.reset_dropdown)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)

  def birthday_drop_down_changed(self, widget, value):
    self.clear_errors()
    if value == "Add a birthday":
      self.dialog = gui.GenericDialog(title="＋ Add a birthday",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      self.name = gui.Label("Name: ", width=200, height=30, style=LABEL_STYLES)
      self.textinput = gui.TextInput(width=200,
                                     height=30,
                                     style=TEXT_INPUT_STYLES)
      self.birthday = gui.Label("Birthday: ",
                                width=200,
                                height=30,
                                style=LABEL_STYLES)
      self.textinput2 = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.name)
      self.dialog.add_field("name", self.textinput)
      self.dialog.add_field("label2", self.birthday)
      self.dialog.add_field("birthday", self.textinput2)
      self.dialog.confirm_dialog.connect(self.add_birthday)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Remove a birthday":
      self.dialog = gui.GenericDialog(title="✘ Remove a birthday",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      choices = "Saved Birthdays: "
      data = self.assistant.birthdays
      for key in data:
        choices = choices + key + ", "
      choices = choices[0:-2]
      self.dialog.add_field(
        "labels",
        gui.Label(choices, width=400, height=30, style=LABEL_STYLES),
      )
      self.name = gui.Label("Name: ",
                            width=200,
                            height=30,
                            style=LABEL_STYLES)
      self.textinput = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.name)
      self.dialog.add_field("name", self.textinput)
      self.dialog.confirm_dialog.connect(self.remove_birthday)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Get birthday":
      self.dialog = gui.GenericDialog(title="🎂 Get Birthday",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      choices = "Saved Birthdays: "
      data = self.assistant.birthdays
      for key in data:
        choices = choices + key + ", "
      choices = choices[0:len(choices) - 2]
      self.dialog.add_field(
        "labels",
        gui.Label(choices, width=400, height=30, style=LABEL_STYLES),
      )
      self.headText = gui.Label("Enter a name: ",
                                width=200,
                                height=30,
                                style=LABEL_STYLES)
      self.dialog.add_field("label", self.headText)
      self.textinput = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label1", self.textinput)
      self.dialog.confirm_dialog.connect(self.get_birthday)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)

  def contact_drop_down_changed(self, widget, value):
    self.clear_errors()
    if value == "Add a contact":
      self.dialog = gui.GenericDialog(title="＋ Add a contact",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      self.name = gui.Label("Name: ", width=200, height=30, style=LABEL_STYLES)
      self.textinput = gui.TextInput(width=200,
                                     height=30,
                                     style=TEXT_INPUT_STYLES)
      self.contact = gui.Label("Title: ",
                               width=200,
                               height=30,
                               style=LABEL_STYLES)
      self.textinput2 = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.name)
      self.dialog.add_field("name", self.textinput)
      self.dialog.add_field("label2", self.contact)
      self.dialog.add_field("contact", self.textinput2)
      self.dialog.confirm_dialog.connect(self.add_contact)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Remove a contact":
      self.dialog = gui.GenericDialog(title="✘ Remove a contact",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      choices = "My Contacts: "
      data = self.assistant.contacts
      for key in data:
        choices = choices + key + ", "
      choices = choices[0:len(choices) - 2]
      self.dialog.add_field(
        "labels",
        gui.Label(choices, width=400, height=30, style=LABEL_STYLES),
      )
      self.name = gui.Label("Name: ",
                            width=200,
                            height=30,
                            style=LABEL_STYLES)
      self.textinput = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label", self.name)
      self.dialog.add_field("name", self.textinput)
      self.dialog.confirm_dialog.connect(self.remove_contact)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)
    elif value == "Get contact":
      self.dialog = gui.GenericDialog(title="👋 Get contact",
                                      width="500px",
                                      style=TITLE_BOX_STYLES)
      data = self.assistant.contacts
      choices = "My Contacts: "
      for key in data:
        choices = choices + key + ", "
      choices = choices[0:len(choices) - 2]
      self.dialog.add_field(
        "labels",
        gui.Label(choices, width=400, height=30, style=LABEL_STYLES),
      )
      self.headText = gui.Label("Enter a name: ",
                                width=200,
                                height=30,
                                style=LABEL_STYLES)
      self.dialog.add_field("label", self.headText)
      self.textinput = gui.TextInput(width=200,
                                      height=30,
                                      style=TEXT_INPUT_STYLES)
      self.dialog.add_field("label1", self.textinput)
      self.dialog.confirm_dialog.connect(self.get_contact)
      self.dialog.cancel_dialog.connect(self.reset_dropdown)
      self.dialog.show(self)

  def main(self):
    with open("todo.json", "r") as todos:
      todo_list = json.load(todos)
      self.assistant = PersonalAssistant(todo_list)

    container = gui.VBox(
      width=500,
      height="auto",
      margin="0px auto",
      style={
        "display": "block",
        "min-height": "300px",
        "overflow": "hidden",
        "box-shadow": "none",
        "border": "1px solid #d7d7d7",
        "padding-bottom": "10px",
      },
    )

    menu = gui.Menu(
      width="100%",
      height="30px",
      style={
        "display": "relative",
        "background-color": "#58CCE0",
        "padding-top": "0",
      },
    )
    menubar = gui.MenuBar(
      width="100%",
      height="30px",
      style={
        "display": "relative",
        "margin-bottom": "16px",
        "padding-top": "0"
      },
    )
    menubar.append(menu)
    container.append(menubar)

    self.errors = gui.ListView()
    self.errors.attributes["class"] += " errors"

    container.append(self.errors)

    self.label = gui.Label("How can I help you?" " 🤖", width=340, height=10)
    self.label.set_style({
      "font-size": "24px",
      "font-family": "'Montserrat', 'Arial', san-serif",
      "font-weight": "bold",
      "color": "#3b3b3b",
      "text-transform": "uppercase",
      "text-align": "center",
      "margin-bottom": "20px",
    })

    self.todoLabel = gui.Label("Manage to-dos", width=250, height=10)
    self.todoLabel.set_style(LABEL_STYLES)
    self.todoDropDown = gui.DropDown.new_from_list(
      ("Select an action", "Add a to-do", "Remove a to-do", "Get to-do list"),
      width=200,
      height=30,
      margin="15px",
    )
    self.todoDropDown.set_style({
      "font-size": "16px",
      "border": "none",
      "background-color": "#f5f5f5"
    })
    self.todoDropDown.select_by_value("")
    self.todoDropDown.onchange.connect(self.todo_drop_down_changed)

    self.birthdayLabel = gui.Label("Manage birthday dates list",
                                   width=250,
                                   height=15)
    self.birthdayLabel.set_style(LABEL_STYLES)
    self.birthdayDropDown = gui.DropDown.new_from_list(
      ("Select an action", "Add a birthday", "Remove a birthday",
       "Get birthday"),
      width=200,
      height=30,
      margin="10px",
    )
    self.birthdayDropDown.set_style({
      "font-size": "16px",
      "border": "none",
      "background-color": "#f5f5f5"
    })
    self.birthdayDropDown.select_by_value("")
    self.birthdayDropDown.onchange.connect(self.birthday_drop_down_changed)

    self.contactsLabel = gui.Label("Manage contacts list",
                                   width=250,
                                   height=15)
    self.contactsLabel.set_style(LABEL_STYLES)

    self.contactDropDown = gui.DropDown.new_from_list(
      ("Select an action", "Add a contact", "Remove a contact", "Get contact"),
      width=200,
      height=30,
      margin="10px",
    )
    self.contactDropDown.set_style({
      "font-size": "16px",
      "border": "none",
      "background-color": "#f5f5f5"
    })
    self.contactDropDown.select_by_value("")
    self.contactDropDown.onchange.connect(self.contact_drop_down_changed)

    container.append(self.label)
    container.append(self.todoLabel)
    container.append(self.todoDropDown)
    container.append(self.birthdayLabel)
    container.append(self.birthdayDropDown)
    container.append(self.contactsLabel)
    container.append(self.contactDropDown)

    # return of the root widget
    return container
