import streamlit as st
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Bootstrap Grid Auto-Grader", layout="wide")

st.title("🎓 Bootstrap Grid Layout Auto-Grader")
st.write("Upload your HTML file to check if it meets the Bootstrap grid requirements")

uploaded_file = st.file_uploader("Choose an HTML file", type=['html'])

def check_bootstrap_link(soup):
    """Check if Bootstrap CSS is linked"""
    links = soup.find_all('link', href=re.compile(r'bootstrap.*\.css'))
    return len(links) > 0, links

def check_container(soup):
    """Check if there's a container class"""
    containers = soup.find_all(class_=re.compile(r'\bcontainer\b'))
    return len(containers) > 0, containers

def check_rows(soup):
    """Check for row classes"""
    rows = soup.find_all(class_=re.compile(r'\brow\b'))
    return len(rows) >= 3, rows

def check_columns(soup):
    """Check for column classes (col-*)"""
    cols = soup.find_all(class_=re.compile(r'\bcol-?\d*\b'))
    return len(cols) >= 8, cols

def check_horizontal_alignment(soup):
    """Check for horizontal alignment classes (justify-content-*)"""
    h_align = soup.find_all(class_=re.compile(r'justify-content-(center|start|end|between|around|evenly)'))
    return len(h_align) >= 2, h_align

def check_vertical_alignment(soup):
    """Check for vertical alignment classes (align-items-*)"""
    v_align = soup.find_all(class_=re.compile(r'align-items-(center|start|end|stretch|baseline)'))
    return len(v_align) >= 3, v_align

def analyze_sections(rows):
    """Analyze each section for specific requirements"""
    sections = []
    
    for idx, row in enumerate(rows, 1):
        section_info = {
            'number': idx,
            'classes': row.get('class', []),
            'columns': len(row.find_all(class_=re.compile(r'\bcol-?\d*\b'))),
            'h_alignment': [cls for cls in row.get('class', []) if 'justify-content' in cls],
            'v_alignment': [cls for cls in row.get('class', []) if 'align-items' in cls]
        }
        sections.append(section_info)
    
    return sections

if uploaded_file is not None:
    html_content = uploaded_file.read().decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    st.success("✅ File uploaded successfully!")
    
    st.header("📊 Grading Results")
    
    # Create scoring system
    total_score = 0
    max_score = 100
    
    # Check 1: Bootstrap CSS Link
    st.subheader("1. Bootstrap CSS Link (10 points)")
    has_bootstrap, links = check_bootstrap_link(soup)
    if has_bootstrap:
        st.success(f"✅ Bootstrap CSS is properly linked ({len(links)} link(s) found)")
        total_score += 10
    else:
        st.error("❌ Bootstrap CSS link not found")
    
    # Check 2: Container
    st.subheader("2. Container Class (15 points)")
    has_container, containers = check_container(soup)
    if has_container:
        st.success(f"✅ Container class found ({len(containers)} container(s))")
        total_score += 15
    else:
        st.error("❌ Container class not found")
    
    # Check 3: Rows
    st.subheader("3. Row Classes (15 points)")
    has_rows, rows = check_rows(soup)
    if has_rows:
        st.success(f"✅ Multiple rows found ({len(rows)} rows)")
        total_score += 15
    else:
        st.warning(f"⚠️ Found {len(rows) if rows else 0} rows (need at least 3)")
        total_score += (len(rows) * 5) if rows else 0
    
    # Check 4: Columns
    st.subheader("4. Column Classes (15 points)")
    has_cols, cols = check_columns(soup)
    if has_cols:
        st.success(f"✅ Multiple columns found ({len(cols)} columns)")
        total_score += 15
    else:
        st.warning(f"⚠️ Found {len(cols) if cols else 0} columns (need at least 8)")
        total_score += min(len(cols) * 2, 15) if cols else 0
    
    # Check 5: Horizontal Alignment
    st.subheader("5. Horizontal Alignment (justify-content-*) (20 points)")
    has_h_align, h_aligns = check_horizontal_alignment(soup)
    if has_h_align:
        st.success(f"✅ Horizontal alignment classes found ({len(h_aligns)} instances)")
        for elem in h_aligns[:3]:
            classes = [cls for cls in elem.get('class', []) if 'justify-content' in cls]
            st.write(f"   - {', '.join(classes)}")
        total_score += 20
    else:
        st.warning(f"⚠️ Found {len(h_aligns) if h_aligns else 0} horizontal alignment classes (need at least 2)")
        total_score += (len(h_aligns) * 10) if h_aligns else 0
    
    # Check 6: Vertical Alignment
    st.subheader("6. Vertical Alignment (align-items-*) (25 points)")
    has_v_align, v_aligns = check_vertical_alignment(soup)
    if has_v_align:
        st.success(f"✅ Vertical alignment classes found ({len(v_aligns)} instances)")
        for elem in v_aligns[:3]:
            classes = [cls for cls in elem.get('class', []) if 'align-items' in cls]
            st.write(f"   - {', '.join(classes)}")
        total_score += 25
    else:
        st.warning(f"⚠️ Found {len(v_aligns) if v_aligns else 0} vertical alignment classes (need at least 3)")
        total_score += (len(v_aligns) * 8) if v_aligns else 0
    
    # Section Analysis
    if rows:
        st.header("🔍 Section-by-Section Analysis")
        sections = analyze_sections(rows)
        
        for section in sections:
            with st.expander(f"Section {section['number']} - {section['columns']} columns"):
                st.write(f"**Row classes:** {', '.join(section['classes'])}")
                st.write(f"**Number of columns:** {section['columns']}")
                st.write(f"**Horizontal alignment:** {', '.join(section['h_alignment']) if section['h_alignment'] else 'None'}")
                st.write(f"**Vertical alignment:** {', '.join(section['v_alignment']) if section['v_alignment'] else 'None'}")
    
    # Final Score
    st.header("🎯 Final Score")
    percentage = (total_score / max_score) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Points Earned", f"{total_score}/{max_score}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        if percentage >= 90:
            grade = "A"
            color = "green"
        elif percentage >= 80:
            grade = "B"
            color = "blue"
        elif percentage >= 70:
            grade = "C"
            color = "orange"
        else:
            grade = "F"
            color = "red"
        st.metric("Grade", grade)
    
    # Progress bar
    st.progress(total_score / max_score)
    
    # Summary
    st.header("📝 Summary")
    if percentage >= 90:
        st.success("🎉 Excellent work! Your Bootstrap grid layout meets all requirements.")
    elif percentage >= 70:
        st.info("👍 Good job! Your layout meets most requirements. Check the feedback above for areas to improve.")
    else:
        st.warning("⚠️ Your layout needs more work. Review the requirements and ensure you have:")
        st.write("- Container class")
        st.write("- Multiple rows (at least 3)")
        st.write("- Multiple columns (at least 8)")
        st.write("- Horizontal alignment classes (justify-content-*)")
        st.write("- Vertical alignment classes (align-items-*)")

else:
    st.info("👆 Please upload an HTML file to begin grading")
    
    st.markdown("---")
    st.subheader("📋 Requirements Checklist")
    st.write("""
    Your HTML file should include:
    - ✓ Bootstrap CSS link
    - ✓ Container class
    - ✓ At least 3 rows with `row` class
    - ✓ At least 8 columns with `col-*` classes
    - ✓ At least 2 horizontal alignment classes (`justify-content-center`, `justify-content-start`, etc.)
    - ✓ At least 3 vertical alignment classes (`align-items-center`, `align-items-end`, etc.)
    """)