#!/usr/bin/env python3
"""
Build English training PPTX from hand-authored deck definitions in training/decks/.
Placeholders {{VM_IP}}, {{HZ_CRED}}, {{LR_CRED}} — {{VM_IP}} stays literal unless S4T_RESOLVE_VM_IP=1.

Output naming: Module{A-I}_<Topic>_EN.pptx (topic-only, no presenter names).
"""
from __future__ import annotations

from pptx import Presentation

from decks.adv_blueprint import slides as adv_blueprint_slides
from decks.adv_faas import slides as adv_faas_slides
from decks.adv_fl import slides as adv_fl_slides
from decks.course_map import slides as course_map_slides
from decks.ext_multiboard import slides as ext_multiboard_slides
from decks.ext_vn import slides as ext_vn_slides
from decks.ext_webservices import slides as ext_webservices_slides
from decks.placeholders import lab_context, substitute_deck
from decks.speaker_notes import enrich_deck
from decks.projection import prepare_deck
from decks.slot1 import slides as slot1_slides
from decks.slot2 import slides as slot2_slides
from decks.slot3 import slides as slot3_slides
from generate_slides import SLIDES_DIR, new_prs
from generate_slides_en import ALLOWED_IMAGES, add_image_slide
from slides_apply import apply_deck

ALLOWED_IMAGES_EXT = ALLOWED_IMAGES

# Canonical deck filenames (Module A–I)
DECK_FILES = {
    "A": "ModuleA_Deploy_IOcloud_EN.pptx",
    "B": "ModuleB_Plugin_Services_EN.pptx",
    "C": "ModuleC_IoT_Computation_EN.pptx",
    "D": "ModuleD_MultiBoard_EN.pptx",
    "E": "ModuleE_VirtualNetworking_EN.pptx",
    "F": "ModuleF_WebServices_WoT_EN.pptx",
    "G": "ModuleG_FederatedLearning_EN.pptx",
    "H": "ModuleH_Blueprint_K3s_EN.pptx",
    "I": "ModuleI_FaaS_Deviceless_EN.pptx",
}

LEGACY_FILENAMES = (
    # Presenter names in filename
    "Slot1_Deploy_IOcloud_EN.pptx",
    "Slot2_Plugin_Services_EN.pptx",
    "Slot3_IoT_Computation_EN.pptx",
    # Old Slot/Ext/Adv scheme
    "Slot1_Deploy_IOcloud_EN.pptx",
    "Slot2_Plugin_Services_EN.pptx",
    "Slot3_IoT_Computation_EN.pptx",
    "Ext_MultiBoard_EN.pptx",
    "Ext_VirtualNetworking_EN.pptx",
    "Ext_WebServices_EN.pptx",
    "Adv_FederatedLearning_EN.pptx",
    "Adv_Blueprint_EN.pptx",
    "Adv_FaaS_Deviceless_EN.pptx",
)


def _tag_notes(notes: str, tag: str, mins: int) -> str:
    # Presenter reads notes verbatim — no tier/timing header in the script.
    return notes


def _prepare(items, tag: str, mins: int = 4):
    out = []
    for item in items:
        kind = item[0]
        notes_idx = {"title": 4, "section": 3, "theory": 4, "demo": 3, "content": 3, "hands_on": 3,
                     "warn": 3, "code": 3, "image": 4}.get(kind, 3)
        notes = item[notes_idx] if len(item) > notes_idx else ""
        hand_mins = 6 if kind == "hands_on" else mins
        tagged = _tag_notes(notes, tag, hand_mins)
        row = list(item)
        if len(row) > notes_idx:
            row[notes_idx] = tagged
        else:
            row.append(tagged)
        out.append(tuple(row))
    return out


def _save(name: str, items, tag: str, mins: int = 60):
    import generate_slides_en as gse
    gse.ALLOWED_IMAGES = ALLOWED_IMAGES_EXT
    ctx = lab_context()
    resolved = substitute_deck(items, ctx)
    resolved = prepare_deck(resolved)
    resolved = enrich_deck(resolved)
    prs = new_prs()
    apply_deck(prs, _prepare(resolved, tag, mins), add_image=add_image_slide)
    out = SLIDES_DIR / name
    prs.save(str(out))
    ip_note = ctx.get("{{VM_IP}}", "?")
    print(f"Saved {out} ({len(prs.slides)} slides) · placeholder={ip_note}")
    return out


def main():
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    for legacy in LEGACY_FILENAMES:
        p = SLIDES_DIR / legacy
        if p.exists():
            p.unlink()
            print(f"Removed legacy {p.name}")

    decks = [
        _save("00_Course_Map_EN.pptx", course_map_slides(), "CORE", 5),
        _save(DECK_FILES["A"], slot1_slides(), "CORE", 60),
        _save(DECK_FILES["B"], slot2_slides(), "CORE", 60),
        _save(DECK_FILES["C"], slot3_slides(), "CORE", 60),
        _save(DECK_FILES["D"], ext_multiboard_slides(), "EXT", 45),
        _save(DECK_FILES["E"], ext_vn_slides(), "EXT", 45),
        _save(DECK_FILES["F"], ext_webservices_slides(), "EXT", 35),
        _save(DECK_FILES["G"], adv_fl_slides(), "ADV", 75),
        _save(DECK_FILES["H"], adv_blueprint_slides(), "ADV", 50),
        _save(DECK_FILES["I"], adv_faas_slides(), "ADV", 35),
    ]
    total = sum(len(Presentation(str(p)).slides) for p in decks)
    print(f"Done — {len(decks)} decks, {total} slides total")


if __name__ == "__main__":
    main()
