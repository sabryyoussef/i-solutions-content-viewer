"""
I-Solutions Content Viewer
Interactive Streamlit app to showcase scraped content for client presentation
"""

import streamlit as st
import json
import os
from pathlib import Path
from PIL import Image

# Page config
st.set_page_config(
    page_title="I-Solutions - Content Viewer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for I-Solutions branding
st.markdown("""
    <style>
    /* Homepage Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1a73e8 0%, #34a853 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(26, 115, 232, 0.3);
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.4rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Navigation Bar */
    .nav-bar {
        background-color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .nav-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    .nav-link {
        color: #1a73e8;
        text-decoration: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .nav-link:hover {
        background-color: #f8f9fa;
    }
    
    /* Statistics Section */
    .stats-section {
        background-color: #f8f9fa;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 3rem;
    }
    .stats-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 1.1rem;
        color: #5f6368;
        font-weight: 500;
    }
    
    /* Course Cards */
    .course-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    .course-card {
        background-color: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .course-card:hover {
        transform: translateY(-5px);
    }
    .course-header {
        background: linear-gradient(135deg, #1a73e8, #34a853);
        color: white;
        padding: 1.5rem;
        text-align: center;
    }
    .course-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .course-price {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .course-body {
        padding: 1.5rem;
    }
    .course-description {
        color: #5f6368;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .enroll-btn {
        background-color: #1a73e8;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .enroll-btn:hover {
        background-color: #1557b0;
    }
    
    /* Buttons */
    .btn-primary {
        background-color: #1a73e8;
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        border: none;
        font-weight: bold;
        margin: 0.5rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        font-size: 1.1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    .btn-primary:hover {
        background-color: #1557b0;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4);
    }
    .btn-secondary {
        background-color: transparent;
        color: #1a73e8;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        border: 2px solid #1a73e8;
        font-weight: bold;
        margin: 0.5rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .btn-secondary:hover {
        background-color: #1a73e8;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Original styles for other pages */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5f6368;
        text-align: center;
        margin-bottom: 2rem;
    }
    .service-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        border-left: 4px solid #1a73e8;
    }
    .testimonial-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #e8f4fd;
        margin-bottom: 1rem;
        border-left: 4px solid #34a853;
    }
    .faq-card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #fff9e6;
        margin-bottom: 1rem;
    }
    .stat-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #e8f5e9;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Paths
BASE_DIR = Path(__file__).parent
SCRAPED_DIR = BASE_DIR / "data"
CONTENT_DIR = SCRAPED_DIR / "content"
IMAGES_DIR = BASE_DIR / "static" / "images"

# Load JSON data
@st.cache_data
def load_json(filename):
    """Load JSON file"""
    filepath = CONTENT_DIR / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None

# Load data
homepage_content = load_json('homepage_content.json')
links = load_json('links.json')
images_inventory = load_json('images_inventory.json')

# Sidebar navigation
st.sidebar.title("🎓 I-Solutions")
st.sidebar.markdown("### Content Viewer")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "📊 Overview",
        "📝 Services",
        "⭐ Testimonials",
        "❓ FAQs",
        "🖼️ Images Gallery",
        "📞 Contact & Social",
        "📋 Raw Data"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
    **Purpose**: This viewer showcases all scraped content 
    from I-Solutions website for integration into Odoo 18 module.
    
    **Status**: ✅ Ready for Demo
""")

# Main content based on page selection
if page == "📊 Overview":
    # Hero Section - Like the actual website
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🎓 Transform Your Career with World-Class Training Programs</div>
        <div class="hero-subtitle">Join thousands of professionals who accelerated their growth with our expert-led courses and internationally recognized certifications.</div>
        <a href="#" class="btn-primary">Find Your Perfect Course</a>
        <a href="#" class="btn-secondary">View Training Schedule</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo Section
    logo_path = IMAGES_DIR / "logos" / "shrm-logo.svg"
    if logo_path.exists():
        st.image(str(logo_path), width=200)
    
    # Navigation Bar
    st.markdown("""
    <div class="nav-bar">
        <div class="nav-links">
            <a href="#" class="nav-link">For Organizations</a>
            <a href="#" class="nav-link">Training Courses</a>
            <a href="#" class="nav-link">Diplomas</a>
            <a href="#" class="nav-link">About Us</a>
            <a href="#" class="nav-link">Blog</a>
            <a href="#" class="nav-link">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Featured Programs Section
    st.markdown("### 🏆 Featured Programs & Certifications")
    st.markdown("---")
    
    # Course Cards Grid with actual images
    courses = [
        {
            "title": "Cybersecurity",
            "certification": "ATD",
            "price": "SAR 3,500",
            "description": "Master cybersecurity fundamentals and protect digital assets.",
            "image": "cert_cybersecurity.jpg"
        },
        {
            "title": "SHRM Advanced Certificate",
            "certification": "SHRM-ACHRM", 
            "price": "SAR 4,200",
            "description": "Advanced human resource management certification program.",
            "image": "cert_shrm.jpg"
        },
        {
            "title": "Financial Accounting",
            "certification": "FMAA",
            "price": "SAR 2,800",
            "description": "Comprehensive financial and managerial accounting preparation.",
            "image": "cert_accounting.jpg"
        },
        {
            "title": "Project Management",
            "certification": "PMP",
            "price": "SAR 3,800",
            "description": "Project Management Professional certification preparation.",
            "image": "cert_pmp.jpg"
        },
        {
            "title": "AI Consultant",
            "certification": "AI",
            "price": "SAR 4,500",
            "description": "Certified Artificial Intelligence Consultant preparation.",
            "image": "cert_ai.jpg"
        },
        {
            "title": "Professional Training",
            "certification": "CPTD",
            "price": "SAR 3,200",
            "description": "Certified Professional in Talent Development program.",
            "image": "cert_training.jpg"
        }
    ]
    
    st.markdown('<div class="course-grid">', unsafe_allow_html=True)
    
    for i in range(0, len(courses), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(courses):
                course = courses[i + j]
                with col:
                    # Display course image
                    image_path = IMAGES_DIR / course['image']
                    if image_path.exists() and image_path.stat().st_size > 1000:  # Only show if file has content
                        st.image(str(image_path), width=300, caption=course['title'])
                    else:
                        st.info(f"📚 {course['title']}")
                    
                    st.markdown(f"""
                    <div class="course-card">
                        <div class="course-header">
                            <div class="course-title">{course['title']}</div>
                            <div class="course-price">{course['price']}</div>
                        </div>
                        <div class="course-body">
                            <div class="course-description">{course['description']}</div>
                            <button class="enroll-btn">ENROLL NOW</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # I-Solutions in Numbers
    st.markdown("""
    <div class="stats-section">
        <div class="stats-title">📊 I-Solutions in Numbers</div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">12+</div>
                <div class="stat-label">Years of Experience</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">9,500+</div>
                <div class="stat-label">People Trained</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">350</div>
                <div class="stat-label">Clients Served</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">94%</div>
                <div class="stat-label">Client Satisfaction</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">650+</div>
                <div class="stat-label">Coaching Hours</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Partner Logos Section
    st.markdown("### 🤝 Our Partners & Certifications")
    st.markdown("---")
    
    # Display partner logos
    logos_dir = IMAGES_DIR / "logos"
    if logos_dir.exists():
        logo_files = list(logos_dir.glob("partners_logo-*.png"))[:8]  # Show first 8 logos
        
        if logo_files:
            cols = st.columns(4)
            for i, logo_file in enumerate(logo_files):
                with cols[i % 4]:
                    st.image(str(logo_file), width=120, caption="")
    
    # Search Section
    st.markdown("""
    <div class="search-section">
        <div class="search-title">🔍 Start Your Learning Journey Today</div>
        <input type="text" class="search-input" placeholder="Search for courses, certifications, or programs...">
    </div>
    """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("### About I-Solutions")
    st.markdown("""
    I-Solutions is a leading training and development company, offering specialized learning experiences 
    designed to empower individuals and organizations. We provide world-class training programs that help 
    professionals transform their careers and achieve sustainable success.
    """)
    
    # Mission
    st.markdown("### 🎯 Our Mission")
    st.markdown("""
    > We aim to unleash the potential of individuals and organizations to achieve outstanding performance 
    > and attain remarkable outcomes through expert-led training and internationally recognized certifications.
    """)
    
    # Footer-like section
    st.markdown("""
    <div class="footer-section">
        <div class="footer-title">Ready to Transform Your Career?</div>
        <p style="text-align: center; font-size: 1.1rem; margin: 2rem 0;">
            Join thousands of professionals who have accelerated their growth with our programs.
        </p>
        <div style="text-align: center;">
            <a href="#" class="btn-primary">Get Started Today</a>
            <a href="#" class="btn-secondary">Contact Our Experts</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Info box
    st.info("💡 **For Odoo Integration**: This homepage layout will be recreated in Odoo using website templates, course catalogs, and e-commerce integration for I-Solutions")

elif page == "📝 Services":
    st.markdown('<div class="main-header">Our Services</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    services = [
        {
            "number": "01",
            "name": "HR Development",
            "description": "Through our collaboration with SHRM, we specialize in offering bespoke HR development programs, aimed at empowering professionals of all levels.",
            "icon": "👥"
        },
        {
            "number": "02",
            "name": "Leadership Development",
            "description": "Unleash your leadership potential with our customized leadership development journeys. Experience tailored programs for leaders at all levels.",
            "icon": "🎯"
        },
        {
            "number": "03",
            "name": "Professional Skills Development",
            "description": "Experience our Professional Skills Development service tailored to enhance soft skills. We specialize in delivering self-development, team skills, and future-oriented programs.",
            "icon": "💡"
        },
        {
            "number": "04",
            "name": "Training Consulting Services",
            "description": "Elevate your workforce with our comprehensive suite of Training Consulting Services, with tailored solutions to bridge knowledge and skill gaps, ensuring your workforce thrives.",
            "icon": "📊"
        },
        {
            "number": "05",
            "name": "Fresh Graduates Development",
            "description": "Prepare for professional success with our Fresh Graduates Development Service. We provide tailored programs combining mentorship, skills training, and career guidance to equip graduates for the workforce.",
            "icon": "🎓"
        },
        {
            "number": "06",
            "name": "Coaching",
            "description": "Unlock your potential with personalized coaching by our certified experts. Receive tailored guidance for personal and professional growth.",
            "icon": "🎯"
        }
    ]
    
    for service in services:
        st.markdown(f"""
        <div class="service-card">
            <h2>{service['icon']} Service {service['number']} - {service['name']}</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">{service['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 **For Odoo Integration**: Each service will become a `slide.tag` (course category) for I-Solutions")

elif page == "⭐ Testimonials":
    st.markdown('<div class="main-header">Client Testimonials</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    testimonials = [
        {
            "client": "National eLearning Center",
            "author": "Dr. Rami I. Alsakran",
            "position": "Deputy Director General for Planning & Development",
            "project": "Organizational Transformation Strategy",
            "quote": """At the National eLearning Center, we worked with Tharwah on an essential project which was the Organizational Transformation Strategy. During our engagement with Tharwah, we had an excellent experience as the project team and leadership from Tharwah pushed beyond the limits to meet our requirements and needs.

Tharwah uses best-fit global practices and methodologies in carrying out their consultancy work. What we liked the most is their flexibility, attention to details, and passion to deliver high quality which exceeded the expectations. We won't hesitate to work with Tharwah again in future projects."""
        },
        {
            "client": "National Events Center",
            "author": "Eng. Feras Al-Babtain",
            "position": "Head of Organization Development & Employee Engagement",
            "project": "Organizational Development",
            "quote": """At the National Events Center, we worked with Tharwah on an Organizational development project, and during our engagement, we had an amazing experience. Tharwah uses best-fit global practices and methodologies in carrying out the consultancy work. What we liked the most is their flexibility, accessibility and diversity of tools, attention to details and passion to deliver high quality. We hope to continue working with them on other projects in the future."""
        }
    ]
    
    for idx, testimonial in enumerate(testimonials, 1):
        st.markdown(f"""
        <div class="testimonial-card">
            <h3>💼 {testimonial['client']}</h3>
            <p><strong>Project:</strong> {testimonial['project']}</p>
            <hr>
            <p style="font-size: 1.1rem; line-height: 1.8; font-style: italic;">
            "{testimonial['quote']}"
            </p>
            <hr>
            <p><strong>{testimonial['author']}</strong><br>
            <em>{testimonial['position']}</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 **For Odoo Integration**: Testimonials will be created as `blog.post` records for I-Solutions")

elif page == "❓ FAQs":
    st.markdown('<div class="main-header">Frequently Asked Questions</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    faqs = [
        {
            "q": "What is I-Solutions?",
            "a": "I-Solutions is a leading training and development company, offering specialized learning experiences designed to empower individuals and organizations."
        },
        {
            "q": "What services does I-Solutions offer?",
            "a": "We offer a variety of training tracks and HR certifications, in addition to a comprehensive range of customized learning solutions for organizations, covering areas such as coaching, training consulting services, and professional skills development."
        },
        {
            "q": "Who delivers the training courses at I-Solutions?",
            "a": "Training is delivered by experienced professionals and certified experts with deep knowledge in their respective fields."
        },
        {
            "q": "Do you work with individuals or only organizations?",
            "a": "We support both individuals looking to grow professionally and organizations seeking to develop their workforce capabilities."
        },
        {
            "q": "Can training courses be customized based on the organization's needs?",
            "a": "Yes, we offer customized training courses tailored to your company's nature and employee levels to ensure maximum benefit."
        },
        {
            "q": "Do you offer in-person or virtual training?",
            "a": "We offer flexible training formats, including in-person, virtual, and blended learning to suit different needs and preferences."
        },
        {
            "q": "Does the Academy provide accredited certificates upon completion of training courses?",
            "a": "Yes, we collaborate with internationally recognized training institutions to ensure that participants receive globally accredited certificates."
        },
        {
            "q": "Where are your offices located?",
            "a": "Our head office is in Riyadh, in the Al-Narjis district, and we proudly serve our clients from additional locations in Jeddah, Dammam, Dubai, and Egypt."
        }
    ]
    
    for idx, faq in enumerate(faqs, 1):
        with st.expander(f"**{idx}. {faq['q']}**"):
            st.write(faq['a'])
    
    st.info("💡 **For Odoo Integration**: FAQs can be added to website pages or help content")

elif page == "🖼️ Images Gallery":
    st.markdown('<div class="main-header">Images Gallery</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    if images_inventory:
        # Show image categories
        tab1, tab2, tab3 = st.tabs(["📋 Logos & Partners", "🎨 Backgrounds", "📊 Statistics"])
        
        with tab1:
            st.subheader("Logos & Partner Images")
            if images_inventory.get('logos'):
                st.success(f"✅ **{len(images_inventory['logos'])} logos downloaded**")
                
                cols = st.columns(4)
                for idx, img_data in enumerate(images_inventory['logos']):
                    with cols[idx % 4]:
                        img_path = IMAGES_DIR / "logos" / img_data['filename']
                        if img_path.exists():
                            try:
                                image = Image.open(img_path)
                                st.image(image, caption=img_data['filename'], use_container_width=True)
                                st.caption(f"Alt: {img_data['alt']}")
                            except:
                                st.warning(f"Could not load: {img_data['filename']}")
        
        with tab2:
            st.subheader("Background Images & Service Photos")
            
            # Show service images
            if images_inventory.get('services'):
                st.write("**Service Images:**")
                for img_data in images_inventory['services']:
                    img_path = IMAGES_DIR / "services" / img_data['filename']
                    if img_path.exists():
                        try:
                            image = Image.open(img_path)
                            st.image(image, caption=f"Service Image: {img_data['alt']}", use_container_width=True)
                        except:
                            st.warning(f"Could not load: {img_data['filename']}")
            
            # Show misc images (backgrounds)
            if images_inventory.get('misc'):
                st.write("**Miscellaneous Images:**")
                cols = st.columns(3)
                for idx, img_data in enumerate(images_inventory['misc']):
                    with cols[idx % 3]:
                        img_path = IMAGES_DIR / "misc" / img_data['filename']
                        if img_path.exists() and img_data['filename'].endswith(('.jpg', '.png')):
                            try:
                                image = Image.open(img_path)
                                st.image(image, caption=img_data['filename'], use_container_width=True)
                            except:
                                pass
        
        with tab3:
            st.subheader("📊 Image Statistics")
            
            total_images = sum(len(images_inventory.get(cat, [])) for cat in ['logos', 'services', 'clients', 'accreditation', 'banners', 'misc'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Images", total_images)
            with col2:
                st.metric("Logos", len(images_inventory.get('logos', [])))
            with col3:
                st.metric("Miscellaneous", len(images_inventory.get('misc', [])))
            
            # Show breakdown
            st.write("**Category Breakdown:**")
            for category, imgs in images_inventory.items():
                if imgs:
                    st.write(f"- **{category.capitalize()}**: {len(imgs)} images")

elif page == "📞 Contact & Social":
    st.markdown('<div class="main-header">Contact & Social Media</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📞 Contact Information")
        st.write("**Phone:**")
        st.info("9200-19-590")
        
        st.write("**Registration Number:**")
        st.info("1010929460")
        
        st.write("**Messaging:**")
        st.write("- WhatsApp")
        st.write("- Instagram DM")
        st.write("- Telegram")
    
    with col2:
        st.subheader("🌐 Social Media Links")
        
        if links and links.get('social_media'):
            # Deduplicate social media links
            social_dict = {}
            for social in links['social_media']:
                social_dict[social['platform']] = social['url']
            
            for platform, url in social_dict.items():
                if platform == 'linkedin':
                    st.markdown(f"**LinkedIn**: [View Profile]({url})")
                elif platform == 'twitter':
                    st.markdown(f"**Twitter/X**: [View Profile]({url})")
                elif platform == 'instagram':
                    st.markdown(f"**Instagram**: [View Profile]({url})")
                elif platform == 'youtube':
                    st.markdown(f"**YouTube**: [View Channel]({url})")
    
    st.markdown("---")
    st.success("✅ All contact and social media information extracted successfully!")

elif page == "📋 Raw Data":
    st.markdown('<div class="main-header">Raw Scraped Data</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📄 Homepage Content", "🔗 Links", "🖼️ Images Inventory"])
    
    with tab1:
        st.subheader("Homepage Content JSON")
        if homepage_content:
            st.json(homepage_content)
        else:
            st.error("Failed to load homepage_content.json")
    
    with tab2:
        st.subheader("Links JSON")
        if links:
            st.json(links)
        else:
            st.error("Failed to load links.json")
    
    with tab3:
        st.subheader("Images Inventory JSON")
        if images_inventory:
            st.json(images_inventory)
        else:
            st.error("Failed to load images_inventory.json")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #5f6368; padding: 1rem;">
    <p><strong>I-Solutions Content Viewer</strong></p>
    <p>Content scraped from https://academy.tharwah.net/</p>
    <p>For Odoo 18 E-Learning Module Integration</p>
    <p style="font-size: 0.8rem;">© 2025 I-Solutions. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

