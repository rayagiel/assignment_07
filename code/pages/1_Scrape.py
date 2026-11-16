"""
1_Scrape.py — Part 1: scrape the rivals' menus into one dataset.

The owner picks the cafés, clicks Scrape, and sees what came back: how much was
scraped, every row in one table, and a download of the dataset.

The scraping itself runs in a separate program (code/scrape_menus.py) that
runner.py starts for you — Streamlit and Playwright do not share a process well.
This page only asks for it and shows the result.

Test it: pytest tests/test_pipeline.py -k scrape_page
"""

import os

import pandas as pd
import streamlit as st

from rivals import CAFES, MENUS_FILE, OUR_CAFE, run_scraper

# --- The page: the algorithm, step by step ------------------------------------------
#
# Write the code for each step below its comment. The tests
# (pytest tests/test_pipeline.py -k scrape_page) check the title, the widget keys,
# the metric labels and values, and that Scrape runs run_scraper() with the cafés
# that were picked. Run the whole app (open code/menu_app.py, then Run and Debug ->
# "Streamlit Run: Current File") and click "Scrape" in the sidebar.
#
# 1. HEADING
#    st.title: Salt City: Scrape the Rivals
#    st.markdown: one sentence, e.g. "Pick the cafés to scrape. Each run replaces
#    the saved dataset."
st.title("Salt City: Scrape the Rivals")
st.markdown("Pick the cafés to scrape. Each run replaces the saved dataset.")
#
# 2. PICK AND SCRAPE
#    a. cafes <- st.multiselect labeled "Cafés", key "cafes", options list(CAFES),
#       every café selected by default.
cafe = st.multiselect("Cafes", key="cafes", options=list(CAFES), default=list(CAFES))
#    b. A st.button labeled "Scrape", key "scrape". When it is clicked and at least
#       one café is picked:

button1 = st.button("Scape", key="scrape")
if cafe and button1:
    #          result <- run_scraper(cafes), inside `with st.spinner(...)` — a browser
    #                    visits every café, which takes a few seconds each.
    with st.spinner("..."):
        result = run_scraper(cafe)
#          result.returncode is 0 -> st.success with the LAST line of result.stdout
#                                    (the scraper's "Wrote ... rows" message)
        if result.returncode == 0:
            st.success(f"Wrote {result.stdout} rows")
#          otherwise              -> st.error saying the scraper failed, and
#                                    st.code(the end of result.stderr) — the
#                                    Python error, so you can fix it.
        else:
            st.error("Scraper Failed")
            st.code(result.stderr)
#
# 3. NOTHING TO SHOW YET?
#    If MENUS_FILE does not exist: st.info("No menus yet — ...") and st.stop().
if not os.path.exists(MENUS_FILE):
    st.info("No menus yet -...")
    st.stop()
#
# 4. THE DATASET
#    menus <- pd.read_csv(MENUS_FILE); theirs <- the rows whose cafe is not OUR_CAFE
menus = pd.read_csv(MENUS_FILE)
theirs = menus[menus["cafe"] != OUR_CAFE].copy()
#    Three st.metric cards side by side (st.columns(3)), all about `theirs`:
#       "Cafés": how many different cafés   "Items": how many different
#       (cafe, item) pairs                  "Rows": how many rows (one per size)
col1, col2, col3 = st.columns(3)
with col1:
    cafes = theirs["cafe"].nunique()
    st.metric("Cafés", cafes)
with col2:
    pairs = len(theirs[["cafe", "item"]].drop_duplicates())
    st.metric("Items", pairs)
with col3:
    st.metric("Rows", len(theirs))
#    st.dataframe(menus, hide_index=True)
st.dataframe(menus, hide_index=True)
#    st.download_button "Download the dataset" with menus.to_csv(index=False),
#       file_name "menus.csv", mime "text/csv", key "download"
export_final = menus.to_csv(index=False)
st.download_button(
        key="download",
        label="Download the dataset",
        data=export_final,
        mime="text/csv"
    )
