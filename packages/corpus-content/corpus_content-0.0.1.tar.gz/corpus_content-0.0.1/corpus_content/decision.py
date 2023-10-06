from pathlib import Path
from typing import NamedTuple

import frontmatter
from citation_utils import Citation

from .author import get_writer_from_path
from .opinion import Opinion


class Decision(NamedTuple):
    id: str
    citation: Citation
    title: str
    main_opinion: Opinion
    separate_opinions: list[Opinion]
    short: str | None = None
    justice_id: int | None = None
    curiam: bool = False
    category: str | None = None
    composition: str | None = None

    def __repr__(self) -> str:
        return f"<Decision {self.id}>"

    @property
    def citation_row(self):
        data = self.citation.make_docket_row()
        if not data:
            raise Exception("Could not generate citation data")
        data.pop("id")
        return data

    @property
    def case_row(self):
        return {
            "id": self.id,
            "category": self.category,
            "composition": self.composition,
            "title": self.title,
            "short": self.short,
            "justice_id": self.justice_id,
            "curiam": self.curiam,
        }

    @classmethod
    def from_file(cls, file: Path):
        # initialize
        separate_opinions = []
        opdir = file.parent.joinpath("opinion")
        cat, num, date, _ = file.parts[-4:]
        meta = frontmatter.load(file)

        # generate id
        cite = Citation.from_docket_row(
            cat=cat,
            num=num,
            date=date,
            opt_phil=meta.get("phil"),
            opt_scra=meta.get("scra"),
            opt_offg=meta.get("offg"),
        )
        id = cite.set_slug()
        if not id:
            raise Exception("Could not generate decision id.")

        # generate opinions
        if opdir.exists():
            for op_file in opdir.glob("*.md"):
                writer = get_writer_from_path(op_file)
                justice_id = int(writer.justice_digit) if writer.justice_digit else None
                op_filemeta = frontmatter.load(op_file)
                separate_opinions.append(
                    Opinion(
                        id=f"{id}-{file.stem}",
                        decision_id=id,
                        content=op_filemeta.content,
                        justice_id=justice_id,
                        is_main=False,
                        label=op_filemeta.get("label", "Opinion"),
                        file_statutes=op_filemeta.get("statutes"),
                        file_citations=op_filemeta.get("citations"),
                    )
                )

        # create main_opinion
        authorship = get_writer_from_path(file)
        main_opinion = Opinion(
            id=f"{id}-main",
            decision_id=id,
            content=meta.content,
            justice_id=authorship.justice_digit,
            is_main=True,
            label="Main",
            file_statutes=meta.get("statutes"),
            file_citations=meta.get("citations"),
        )

        # collect all fields
        return cls(
            id=id,
            citation=cite,
            title=meta.get("title"),
            short=meta.get("short"),
            main_opinion=main_opinion,
            separate_opinions=separate_opinions,
            justice_id=authorship.justice_digit,
            curiam=authorship.curiam,
            category=meta.get("category"),
            composition=meta.get("composition"),
        )
