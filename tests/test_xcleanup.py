import pathlib
import sys

import pytest


def test_help_flag_prints_usage(capsys, monkeypatch, load_tool_module):
    module = load_tool_module("xcleanup")

    monkeypatch.setattr(sys, "argv", ["xcleanup", "--help"])
    module.main()

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "remove-meme-images" in captured.out
    assert captured.err == ""


def test_remove_meme_images_deletes_only_matching_images(
    tmp_path, capsys, load_tool_module
):
    module = load_tool_module("xcleanup")
    public_dir = tmp_path / "public"
    public_dir.mkdir()

    removable = [
        public_dir / "charlie-launch.png",
        public_dir / "meme-draft.jpg",
    ]
    keepers = [
        public_dir / "logo.png",
        public_dir / "notes.txt",
        public_dir / "banner.webp",
    ]

    for path in removable + keepers:
        path.write_text("stub", encoding="utf-8")

    removed = module.remove_meme_images(str(public_dir))

    captured = capsys.readouterr()
    assert sorted(pathlib.Path(path).name for path in removed) == [
        "charlie-launch.png",
        "meme-draft.jpg",
    ]
    assert "Cleanup complete. Removed 2 file(s)." in captured.out
    for path in removable:
        assert not path.exists()
    for path in keepers:
        assert path.exists()


def test_remove_meme_images_supports_dry_run(tmp_path, capsys, load_tool_module):
    module = load_tool_module("xcleanup")
    public_dir = tmp_path / "public"
    public_dir.mkdir()
    image_path = public_dir / "launch-meme.gif"
    image_path.write_text("stub", encoding="utf-8")

    removed = module.remove_meme_images(str(public_dir), dry_run=True)

    captured = capsys.readouterr()
    assert removed == [str(image_path)]
    assert f"Would remove: {image_path}" in captured.out
    assert image_path.exists()


def test_remove_meme_images_requires_existing_directory(
    tmp_path, load_tool_module
):
    module = load_tool_module("xcleanup")
    missing_dir = tmp_path / "missing-public-dir"

    with pytest.raises(SystemExit) as exc_info:
        module.remove_meme_images(str(missing_dir))

    assert exc_info.value.code == 1
