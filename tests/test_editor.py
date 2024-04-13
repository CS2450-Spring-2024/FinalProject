import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import scrolledtext as scrolledtext
from unittest.mock import patch
from tempfile import NamedTemporaryFile
import os
import pytest

from uvsim.editor import Editor  # Assuming your Editor class is in editor.py


@pytest.fixture
def editor_instance():
    master = tk.Tk()
    editor = Editor(master, None)
    yield editor
    # master.destroy()


def test_open_file(editor_instance):
    with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write("1\n2\n3\n-99999")
        tmp_file_path = tmp_file.name

    with patch.object(filedialog, 'askopenfilename', return_value=tmp_file_path):
        editor_instance.open_file()

    assert editor_instance.text_box.get("1.0", "4.0") == "1\n2\n3\n"

    os.unlink(tmp_file_path)


def test_save(editor_instance):
    content = "1\n2\n3"
    editor_instance.text_box.insert(tk.END, content)

    with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file_path = tmp_file.name

    with patch.object(filedialog, 'asksaveasfile', return_value=NamedTemporaryFile(mode='w', delete=False)) as mock_save_as:
        editor_instance.open_file_path = tmp_file_path
        editor_instance.save()

    with open(tmp_file_path) as f:
        assert f.read()[:5] == content

    os.unlink(tmp_file_path)


def test_save_as(editor_instance):
    content = "1\n2\n3\n-99999"
    editor_instance.text_box.insert(tk.END, content)

    with patch.object(filedialog, 'asksaveasfile', return_value=NamedTemporaryFile(mode='w', delete=False)) as mock_save_as:
        editor_instance.save_as()

    assert editor_instance.open_file_path != ""
    assert editor_instance.text_box.get("1.0", "5.0") == f"{content}\n"


# def test_run(editor_instance):
#     program = "1\n2\n3\n-99999"
#     editor_instance.text_box.insert(tk.END, program)

#     with patch.object(simpledialog, 'askinteger', return_value=None):
#         editor_instance.run()

#     assert editor_instance.parent.memory == {0: '1', 1: '2', 2: '3', 3:'-99999'}


# def test_reset_editor(editor_instance):
#     editor_instance.text_box.insert(tk.END, "Some content")
#     # editor_instance.run()
#     editor_instance.reset_editor()

#     assert editor_instance.text_box.get("1.0", tk.END) == ""