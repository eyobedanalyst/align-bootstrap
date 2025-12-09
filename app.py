import streamlit as st
import requests
import re

# Try to import BeautifulSoup with fallback
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    st.warning("⚠️ beautifulsoup4 is not installed. Some features may be limited.")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Mr Eyobed Sebrala Auto Grader",
        page_icon="📊",
        layout="wide"
    )
    
    # Header
    st.title("Mr Eyobed Sebrala Auto Grader")
    st.markdown("---")
    
    # Check for beautifulsoup4
    if not BEAUTIFULSOUP_AVAILABLE:
        st.error("""
        ❌ **Required package missing!**
        
        Please install beautifulsoup4 by:
        1. Adding it to `requirements.txt`
        2. Or run: `pip install beautifulsoup4==4.12.2`
        """)
        return
    
    # Get user input
    with st.form("github_form"):
        st.subheader("Student Information")
        username = st.text_input("Enter your username:")
        github_link = st.text_input("Enter your GitHub repository link:")
        submit_button = st.form_submit_button("Grade Assignment")
    
    if submit_button and username and github_link:
        grade_assignment(username, github_link)

def grade_assignment(username, github_link):
    """Grade the student's assignment based on requirements"""
    
    st.markdown("---")
    st.subheader(f"Grading Results for: {username}")
    
    # Initialize score
    total_score = 0
    max_score = 10
    results = []
    
    try:
        # Clean and validate GitHub URL
        github_link = clean_github_url(github_link)
        
        # Check if it's a valid GitHub URL
        if not is_valid_github_url(github_link):
            st.error("Invalid GitHub URL. Please provide a valid GitHub repository link.")
            return
        
        # Fetch HTML content from GitHub
        html_content = fetch_html_from_github(github_link)
        
        if not html_content:
            st.error("Could not fetch HTML content from the provided GitHub link.")
            return
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Grade each requirement
        results.append(grade_doctype(soup))
        results.append(grade_container(soup))
        results.append(grade_rows(soup))
        results.append(grade_columns(soup))
        results.append(grade_horizontal_alignment(soup))
        results.append(grade_vertical_alignment(soup))
        results.append(grade_bootstrap_css(soup))
        results.append(grade_bootstrap_js(soup))
        results.append(grade_specific_classes(soup))
        results.append(grade_layout_structure(soup))
        
        # Calculate total score
        total_score = sum([result['score'] for result in results])
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Final Grade", f"{total_score}/{max_score}")
            
        with col2:
            percentage = (total_score / max_score) * 100
            st.metric("Percentage", f"{percentage:.1f}%")
        
        # Display detailed results
        st.markdown("### Detailed Breakdown:")
        
        for result in results:
            with st.expander(f"{result['requirement']} - {result['score']}/{result['max_score']} point(s)"):
                if result['passed']:
                    st.success("✅ " + result['feedback'])
                else:
                    st.error("❌ " + result['feedback'])
                
                if result.get('found_elements'):
                    st.code(result['found_elements'], language='html')
        
        # Display final feedback
        st.markdown("---")
        st.subheader("Final Feedback")
        
        if total_score >= 9:
            st.success("🎉 Excellent work! All requirements are met perfectly!")
        elif total_score >= 7:
            st.info("👍 Good job! Most requirements are met.")
        elif total_score >= 5:
            st.warning("📝 Fair attempt, but needs improvement.")
        else:
            st.error("🚨 Needs significant improvement. Please review the requirements.")
            
    except Exception as e:
        st.error(f"An error occurred during grading: {str(e)}")

def clean_github_url(url):
    """Clean and format GitHub URL"""
    # Remove trailing slash
    url = url.rstrip('/')
    
    # If it's a GitHub repo URL, convert to raw content URL
    if 'github.com' in url and 'blob' in url:
        # Convert to raw URL
        url = url.replace('github.com', 'raw.githubusercontent.com')
        url = url.replace('/blob/', '/')
    
    return url

def is_valid_github_url(url):
    """Check if URL is a valid GitHub URL"""
    github_patterns = [
        r'https?://github\.com/[\w\-]+/[\w\-]+',
        r'https?://raw\.githubusercontent\.com/[\w\-]+/[\w\-]+/[\w\-/\.]+'
    ]
    
    for pattern in github_patterns:
        if re.match(pattern, url):
            return True
    return False

def fetch_html_from_github(url):
    """Fetch HTML content from GitHub"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        # Try alternative approach - look for index.html
        try:
            if 'raw.githubusercontent.com' not in url:
                # Extract user and repo from URL
                match = re.search(r'github\.com/([\w\-]+)/([\w\-]+)', url)
                if match:
                    user, repo = match.groups()
                    raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/index.html"
                    response = requests.get(raw_url, timeout=10)
                    response.raise_for_status()
                    return response.text
        except:
            return None
    return None

def grade_doctype(soup):
    """Check for DOCTYPE declaration"""
    requirement = "DOCTYPE Declaration"
    max_score = 1
    
    if soup.original_encoding and '<!DOCTYPE html>' in str(soup):
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': 'DOCTYPE declaration found.',
            'found_elements': '<!DOCTYPE html>'
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'DOCTYPE declaration missing or incorrect.'
        }

def grade_container(soup):
    """Check for Bootstrap container"""
    requirement = "Bootstrap Container"
    max_score = 1
    
    container = soup.find('div', class_='container')
    if container:
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': 'Bootstrap container found.',
            'found_elements': str(container)[:200] + '...' if len(str(container)) > 200 else str(container)
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'No Bootstrap container found.'
        }

def grade_rows(soup):
    """Check for Bootstrap rows"""
    requirement = "Bootstrap Rows"
    max_score = 1
    
    rows = soup.find_all('div', class_='row')
    if len(rows) >= 4:  # Looking for at least 4 rows as in the example
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': f'Found {len(rows)} Bootstrap rows.',
            'found_elements': '\n\n'.join([str(row)[:150] + '...' for row in rows[:3]])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': f'Only found {len(rows)} row(s). Expected at least 4.'
        }

def grade_columns(soup):
    """Check for Bootstrap columns"""
    requirement = "Bootstrap Columns"
    max_score = 1
    
    # Look for various column classes
    col_classes = ['col-1', 'col-2', 'col-3', 'col-4', 'col-5', 'col-6', 
                   'col-7', 'col-8', 'col-9', 'col-10', 'col-11', 'col-12']
    
    columns = []
    for col_class in col_classes:
        columns.extend(soup.find_all(class_=lambda x: x and col_class in x.split()))
    
    if len(columns) >= 8:  # Looking for multiple columns
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': f'Found {len(columns)} Bootstrap columns.',
            'found_elements': '\n\n'.join([str(col)[:100] + '...' for col in columns[:5]])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': f'Only found {len(columns)} column(s). Expected multiple columns.'
        }

def grade_horizontal_alignment(soup):
    """Check for horizontal alignment classes"""
    requirement = "Horizontal Alignment"
    max_score = 1
    
    # Check for horizontal alignment classes
    horiz_classes = ['justify-content-center', 'justify-content-start', 
                     'justify-content-end', 'justify-content-between', 
                     'justify-content-around']
    
    found = []
    for h_class in horiz_classes:
        elements = soup.find_all(class_=lambda x: x and h_class in x.split())
        found.extend(elements)
    
    if found:
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': f'Found horizontal alignment classes ({len(found)} instances).',
            'found_elements': '\n'.join([str(element)[:150] for element in found[:3]])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'No horizontal alignment classes found.'
        }

def grade_vertical_alignment(soup):
    """Check for vertical alignment classes"""
    requirement = "Vertical Alignment"
    max_score = 1
    
    # Check for vertical alignment classes
    vert_classes = ['align-items-center', 'align-items-start', 
                    'align-items-end', 'align-items-baseline', 
                    'align-items-stretch']
    
    found = []
    for v_class in vert_classes:
        elements = soup.find_all(class_=lambda x: x and v_class in x.split())
        found.extend(elements)
    
    if found:
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': f'Found vertical alignment classes ({len(found)} instances).',
            'found_elements': '\n'.join([str(element)[:150] for element in found[:3]])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'No vertical alignment classes found.'
        }

def grade_bootstrap_css(soup):
    """Check for Bootstrap CSS inclusion"""
    requirement = "Bootstrap CSS Link"
    max_score = 1
    
    # Check for Bootstrap CSS link
    bootstrap_css_links = soup.find_all('link', href=lambda x: x and 'bootstrap' in x.lower())
    
    if bootstrap_css_links:
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': 'Bootstrap CSS link found.',
            'found_elements': '\n'.join([str(link) for link in bootstrap_css_links])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'Bootstrap CSS link not found.'
        }

def grade_bootstrap_js(soup):
    """Check for Bootstrap JS inclusion"""
    requirement = "Bootstrap JS Script"
    max_score = 1
    
    # Check for Bootstrap JS script
    bootstrap_js_scripts = soup.find_all('script', src=lambda x: x and 'bootstrap' in x.lower())
    
    if bootstrap_js_scripts:
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': 'Bootstrap JS script found.',
            'found_elements': '\n'.join([str(script) for script in bootstrap_js_scripts])
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': 'Bootstrap JS script not found.'
        }

def grade_specific_classes(soup):
    """Check for specific Bootstrap utility classes"""
    requirement = "Bootstrap Utility Classes"
    max_score = 1
    
    # Check for common Bootstrap utility classes
    utility_classes = ['bg-', 'text-', 'p-', 'm-', 'rounded', 'shadow', 'fs-', 'fw-']
    
    found_count = 0
    found_examples = []
    
    for util in utility_classes:
        elements = soup.find_all(class_=lambda x: x and util in x)
        found_count += len(elements)
        if elements and len(found_examples) < 3:
            found_examples.append(str(elements[0])[:150])
    
    if found_count >= 10:  # Looking for multiple utility classes
        return {
            'requirement': requirement,
            'passed': True,
            'score': max_score,
            'max_score': max_score,
            'feedback': f'Found {found_count} Bootstrap utility class instances.',
            'found_elements': '\n\n'.join(found_examples)
        }
    else:
        return {
            'requirement': requirement,
            'passed': False,
            'score': 0,
            'max_score': max_score,
            'feedback': f'Only found {found_count} utility class instances. Expected more.'
        }

def grade_layout_structure(soup):
    """Check overall layout structure"""
    requirement = "Layout Structure"
    max_score = 1
    
    # Check for structured layout with multiple sections
    container = soup.find('div', class_='container')
    if container:
        # Count direct child rows
        rows = container.find_all('div', class_='row', recursive=False)
        
        if len(rows) >= 3:  # At least 3 main sections
            return {
                'requirement': requirement,
                'passed': True,
                'score': max_score,
                'max_score': max_score,
                'feedback': f'Good layout structure with {len(rows)} main sections.',
                'found_elements': f'Container with {len(rows)} direct child rows'
            }
    
    return {
        'requirement': requirement,
        'passed': False,
        'score': 0,
        'max_score': max_score,
        'feedback': 'Layout structure needs improvement. Should have container with multiple row sections.'
    }

if __name__ == "__main__":
    main()