
"""
FLAME DNA - NASA Research Catalog
Scientific library interface.
"""

import streamlit as st

from modules.research_catalog.search_engine import (
    search_publications,
    get_catalog_statistics,
)


def render_catalog():

    st.title("NASA Research Catalog")

    st.caption(
        "Explore NASA scientific publications, "
        "research reports and technical knowledge."
    )

    # ==========================================
    # LIBRARY STATISTICS
    # ==========================================

    stats = get_catalog_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Indexed Publications",
            stats["total_publications"],
        )

    with col2:
        st.metric(
            "Years Represented",
            stats["years_covered"],
        )

    with col3:
        st.metric(
            "Connected Sources",
            stats["sources"],
        )

    st.caption(
        "Statistics reflect locally indexed records, "
        "not the entire NASA archive."
    )

    st.divider()

    # ==========================================
    # SCIENTIFIC SEARCH
    # ==========================================

    st.subheader("Scientific Library")

    keyword = st.text_input(
        "Search NASA publications",
        placeholder=(
            "Search by title, keywords or abstract..."
        ),
        key="catalog_keyword",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        author = st.text_input(
            "Author",
            key="catalog_author",
        )

    with col2:
        year = st.text_input(
            "Publication Year",
            placeholder="e.g. 2024",
            key="catalog_year",
        )

    with col3:
        document_type = st.text_input(
            "Document Type",
            key="catalog_document_type",
        )

    results = search_publications(
        keyword=keyword,
        author=author,
        year=year,
        document_type=document_type,
        limit=500,
    )

    st.markdown(
        f"**{len(results)} publications found**"
    )

    # ==========================================
    # SEARCH RESULTS
    # ==========================================

    if not results:
        st.info(
            "No publications match your search."
        )
        return

    for publication in results:

        title = publication["title"]

        with st.expander(title):

            st.write(
                "**NASA ID:**",
                publication["nasa_id"],
            )

            st.write(
                "**Authors:**",
                publication["authors"] or "Not specified",
            )

            st.write(
                "**Publication Date:**",
                publication["publication_date"]
                or "Not specified",
            )

            st.write(
                "**Document Type:**",
                publication["document_type"]
                or "Not specified",
            )

            st.write("**Abstract:**")

            st.write(
                publication["abstract"]
                or "No abstract available."
            )

            if publication["source_url"]:
                st.link_button(
                    "View NASA Publication",
                    publication["source_url"],
                )
