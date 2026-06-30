# JUARISTI Milling Head Angle Lookup

A Streamlit web app that digitizes the JUARISTI 45° manual milling head angle tables
(X–Z and Y–Z horizontal planes) so operators can instantly look up Neck (C-axis) and
Head (A-axis) values instead of searching printed PDF tables.

## What's included
- `app.py` — the Streamlit application
- `icons_data.py` — the 8 orientation reference images (4 orientations × 2 planes),
  embedded as base64 so the app has zero external image-file dependency — no
  `data/icons/` folder to misplace.
- `data/angles.csv` — full digitized lookup table (1,448 rows: 2 planes × 4 head
  orientations × 181 angle increments from 0° to 90° in 30' steps), parsed directly
  from the supplied JUARISTI PDF tables.

## How to run

```bash
pip install streamlit pandas
streamlit run app.py
```

Then open the local URL Streamlit prints (typically http://localhost:8501).

## How to use
1. Select the machining plane (X–Z or Y–Z).
2. Select the milling head orientation (Right-Down, Left-Down, Left-Up, Right-Up) —
   each option shows the actual head image from the JUARISTI manual so you can match
   it visually against the machine.
3. Enter the required tool angle, either with the slider or by typing degrees +
   minutes (table is tabulated in 30' steps; the app snaps to the nearest entry).
4. The Neck (C-axis) and Head (A-axis) values appear instantly, alongside a
   confirmation panel showing the selected head image again.
5. Expand "View full reference table" to browse/search the complete table for the
   selected plane and orientation.

## Notes
- Data was extracted programmatically from the source PDFs (not retyped by hand) to
  minimize transcription error, then spot-checked against the original tables.
- The UI is built mobile/tablet responsive for shop-floor use as well as desktop use
  in engineering offices.
- This is intended as a digital reference aid — always confirm critical setups
  against the physical machine before running production.
