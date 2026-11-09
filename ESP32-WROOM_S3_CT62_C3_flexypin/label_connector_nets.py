import pcbnew

board = pcbnew.GetBoard()

CONNECTOR_REF = "J11"
X_OFFSET_MM = 1.5
Y_OFFSET_MM = 0.0
TEXT_HEIGHT_MM = 1.0
USE_BOTTOM = True

LAYER = pcbnew.B_SilkS if USE_BOTTOM else pcbnew.F_SilkS

X_OFFSET = pcbnew.FromMM(X_OFFSET_MM)
Y_OFFSET = pcbnew.FromMM(Y_OFFSET_MM)
TEXT_HEIGHT = pcbnew.FromMM(TEXT_HEIGHT_MM)

# Cleanup old labels
to_delete = []
for item in board.GetDrawings():
    if type(item).__name__ != "PCB_TEXT":
        continue
    if item.GetText().endswith("/" + CONNECTOR_REF):
        to_delete.append(item)

for item in to_delete:
    board.Remove(item)

print(f"Removed {len(to_delete)} old labels")

# Add new labels
for fp in board.GetFootprints():
    if fp.GetReference() != CONNECTOR_REF:
        continue

    for pad in fp.Pads():
        net = pad.GetNet()
        if not net:
            continue

        netname = net.GetNetname()
        if not netname or netname.startswith("Net-("):
            continue

        visible_text = f"{netname}/{CONNECTOR_REF}"

        text = pcbnew.PCB_TEXT(board)
        text.SetText(visible_text)
        text.SetLayer(LAYER)
        text.SetTextHeight(TEXT_HEIGHT)
        text.SetTextWidth(TEXT_HEIGHT)

        pos = pad.GetPosition()
        new_pos = pcbnew.VECTOR2I(int(pos.x + X_OFFSET), int(pos.y + Y_OFFSET))
        text.SetPosition(new_pos)

        # Correct mirroring for bottom
        if USE_BOTTOM:
            text.SetTextOrientation(pcbnew.TXT_MIRRORED)
        else:
            text.SetTextOrientation(pcbnew.TXT_HORIZ)

        board.Add(text)

pcbnew.Refresh()
print("Net labels updated successfully with proper mirroring for bottom silkscreen.")
