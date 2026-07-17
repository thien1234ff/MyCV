import os
import sys
import subprocess

# Ensure reportlab is installed
try:
    import reportlab
except ImportError:
    print("ReportLab library not found. Installing via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        import reportlab
        print("ReportLab successfully installed!")
    except Exception as e:
        print(f"Error installing ReportLab: {str(e)}")
        print("Please run: pip install reportlab")
        sys.exit(1)

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_pdf(filename="Hoang_Kim_Thien_CV.pdf"):
    # Check if target file is locked
    if os.path.exists(filename):
        try:
            with open(filename, "ab") as f:
                pass
        except PermissionError:
            old_filename = filename
            filename = filename.replace(".pdf", "_new.pdf")
            print(f"Warning: '{old_filename}' is locked (open in another program). Writing to '{filename}' instead.")

    # Target 2 pages on A4 sheet
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=36,  # 0.5 inch margin
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    color_primary = colors.HexColor("#0F172A")
    color_secondary = colors.HexColor("#475569")
    color_accent = colors.HexColor("#0284C7")
    
    # Custom Paragraph Styles
    style_name = ParagraphStyle(
        'CVName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=color_primary
    )
    
    style_subtitle = ParagraphStyle(
        'CVSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=color_secondary,
        spaceAfter=6
    )
    
    style_contact = ParagraphStyle(
        'CVContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=color_secondary,
        spaceAfter=12
    )
    
    style_section_title = ParagraphStyle(
        'CVSectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=color_primary,
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )
    
    style_item_title = ParagraphStyle(
        'CVItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=color_primary,
        keepWithNext=True
    )
    
    style_item_date = ParagraphStyle(
        'CVItemDate',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=color_secondary,
        keepWithNext=True
    )
    
    style_item_sub = ParagraphStyle(
        'CVItemSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=color_secondary,
        keepWithNext=True
    )
    
    style_item_loc = ParagraphStyle(
        'CVItemLoc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        alignment=TA_RIGHT,
        textColor=color_secondary,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'CVBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        alignment=TA_JUSTIFY,
        textColor=color_secondary
    )
    
    style_bullet = ParagraphStyle(
        'CVBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=color_secondary,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=2
    )

    story = []
    
    # ----------------------------------------------------
    # HEADER
    # ----------------------------------------------------
    header_story = []
    
    style_name_left = ParagraphStyle(
        'CVNameLeft',
        parent=style_name,
        alignment=TA_LEFT
    )
    style_subtitle_left = ParagraphStyle(
        'CVSubtitleLeft',
        parent=style_subtitle,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    style_contact_left = ParagraphStyle(
        'CVContactLeft',
        parent=style_contact,
        alignment=TA_LEFT,
        spaceAfter=0
    )
    
    header_story.append(Paragraph("HOANG KIM THIEN", style_name_left))
    header_story.append(Paragraph("Computer Science Student &amp; Artificial Intelligence Researcher", style_subtitle_left))
    
    contact_text = (
        "Email: <a href='mailto:hkthien@husc.edu.vn'>hkthien@husc.edu.vn</a>  |  "
        "Phone: (+84) 76-265-7225  |  "
        "GitHub: <a href='https://github.com/thien1234ff'>github.com/thien1234ff</a><br/>"
        "LinkedIn: <a href='https://linkedin.com/in/hoangkimthien'>linkedin.com/in/hoangkimthien</a>  |  "
        "Google Scholar: <a href='https://scholar.google.com/citations?user=hoangkimthien'>Google Scholar</a>"
    )
    header_story.append(Paragraph(contact_text, style_contact_left))
    
    avatar_path = "img/avatar/b0bf910b9bf51aab43e4.jpg"
    if os.path.exists(avatar_path):
        avatar_img = Image(avatar_path, width=65, height=65)
    else:
        avatar_img = ""
        print(f"Warning: Avatar image not found at {avatar_path}")
        
    header_data = [[header_story, avatar_img]]
    header_table = Table(header_data, colWidths=[450, 73])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 10))
    
    # Helper function for section separators
    def create_section_title(title):
        p = Paragraph(title.upper(), style_section_title)
        # Line underneath
        t = Table([[""]], colWidths=[523], rowHeights=[1])
        t.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (-1,-1), 1, color_primary),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        return [p, t, Spacer(1, 4)]
        
    # Helper function for dual header row (Title/Role & Date/Location)
    def create_item_header(title, date, sub="", loc=""):
        p_title = Paragraph(title, style_item_title)
        p_date = Paragraph(date, style_item_date)
        
        data = [[p_title, p_date]]
        col_widths = [410, 113]
        
        if sub or loc:
            p_sub = Paragraph(sub, style_item_sub)
            p_loc = Paragraph(loc, style_item_loc)
            data.append([p_sub, p_loc])
            
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    # ----------------------------------------------------
    # CAREER OBJECTIVE
    # ----------------------------------------------------
    story.extend(create_section_title("Career Objective"))
    objective_text = (
        "Seeking research assistantships, graduate opportunities (Master's/PhD), and engineering roles in "
        "Artificial Intelligence, Computer Vision, and Machine Learning. Eager to contribute to efficient deep learning "
        "quantization, edge AI deployment, and text analytics while aiming to develop scalable and accessibility-focused "
        "AI systems for real-world applications."
    )
    story.append(Paragraph(objective_text, style_body))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # EDUCATION
    # ----------------------------------------------------
    story.extend(create_section_title("Education"))
    story.append(create_item_header(
        "University of Sciences, Hue University", "2022 — 2026",
        "Bachelor of Science in Computer Science", "Thua Thien Hue, Vietnam"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Academic Standing:</b> Cumulative GPA of <b>3.83 / 4.00</b> (10-point scale: 9.08 / 10.00).", style_bullet))
    story.append(Paragraph("• <b>Graduation Classification:</b> <b>Excellent</b>.", style_bullet))
    story.append(Paragraph("• <b>Academic Ranking:</b> Ranked <b>2nd</b> among all undergraduate Information Technology students in the cohort (K46).", style_bullet))
    story.append(Paragraph("• <b>Scholarships &amp; Honors:</b> Recipient of the prestigious University Merit-Based Scholarship in every semester for outstanding academic performance.", style_bullet))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # RESEARCH PUBLICATIONS
    # ----------------------------------------------------
    story.extend(create_section_title("Research Publications"))
    story.append(create_item_header(
        "IEEE Conference Proceedings", "Accepted (Forthcoming 2026)",
        "The 9th International Conference on Multimedia Analysis and Pattern Recognition (MAPR)", "Hue, Vietnam"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Paper Title:</b> \"Fast-Converging and Architecture-Agnostic 6-Bit Face Recognition via Gradient Coordination and Refined Data\".", style_bullet))
    story.append(Paragraph("• <b>Authors:</b> <u>Hoang Kim Thien</u> and Le Quang Chien.", style_bullet))
    story.append(Paragraph("• <b>Key Contributions:</b> Developed an architecture-agnostic 6-bit (Q6) quantization framework for deep face recognition. Introduced a β-weighted Mean Squared Error (β-MSE) loss function to align quantized student gradients with a full-precision teacher, along with a stable three-phase training recipe.", style_bullet))
    story.append(Paragraph("• <b>Key Achievements:</b> Replaced massive synthetic training datasets with a compact subset of 53,500 real images (110x fewer). Recovered 102% of the teacher's baseline performance on the AgeDB-30 dataset while achieving <b>57.4x faster convergence</b> (3,135 vs. 180,000 iterations).", style_bullet))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # AWARDS & HONORS
    # ----------------------------------------------------
    story.extend(create_section_title("Awards &amp; Honors"))
    story.append(Paragraph("• <b>Best Paper Award</b> — Faculty Student Scientific Research Conference, University of Sciences, Hue University. (October, 2024)", style_bullet))
    story.append(Paragraph("• <b>Second Prize</b> — WCAG 2.2 Accessible Website Design Competition. (July, 2026)", style_bullet))
    story.append(Paragraph("• <b>Second Prize</b> — University ICPC (International Collegiate Programming Contest) Contest. (March, 2026)", style_bullet))
    story.append(Paragraph("• <b>Consolation Prize</b> — National Mathematical Olympiad in Linear Algebra for University Students. (April, 2025)", style_bullet))
    story.append(Paragraph("• <b>University Merit Scholarships</b> — Awarded in consecutive semesters for top academic performance. (2022 — 2026)", style_bullet))
    
    # ----------------------------------------------------
    # FORCE PAGE BREAK FOR PAGE 2
    # ----------------------------------------------------
    story.append(PageBreak())

    # ----------------------------------------------------
    # PROJECTS & ENGINEERING EXPERIENCE
    # ----------------------------------------------------
    story.extend(create_section_title("Projects &amp; Development Experience"))
    
    # Project 1
    story.append(create_item_header(
        "6-Bit Quantized Face Recognition", "August, 2025 — August, 2026",
        "Undergraduate Thesis Project &amp; Research", "PyTorch, Computer Vision, Model Quantization"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• Implemented low-bit quantization-aware training (QAT) to compress face embeddings to 6-bit representations, achieving a theoretical 5.33x storage size reduction for resource-constrained edge AI devices.", style_bullet))
    story.append(Paragraph("• Evaluated robust performance across multiple backbone networks including iResNet-18, iResNet-50, and MobileFaceNet on standard face verification benchmarks (LFW, CFP-FP, AgeDB-30, CALFW, CPLFW).", style_bullet))
    story.append(Spacer(1, 6))

    # Project 2
    story.append(create_item_header(
        "SmartAgri: Accessible Digital Farming Platform", "June, 2026",
        "Award-Winning Accessibility Design Submission", "Next.js, TailwindCSS, Firebase, OpenAI API, WCAG 2.2"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• Designed a full-stack digital agriculture ecosystem structured for elderly, illiterate, and disabled farmers, implementing a strict \"Accessibility-First\" layout compliant with WCAG 2.2 AA.", style_bullet))
    story.append(Paragraph("• Integrated an AI agricultural advisor bot (via GPT API), a screen-reader compatible layout (Semantic HTML, ARIA regions), custom skip links, focus management, and a natural voice reading toolbar. Won 2nd Prize nationally.", style_bullet))
    story.append(Spacer(1, 6))

    # Project 3
    story.append(create_item_header(
        "Vietnamese Text Summarization Pipeline", "October, 2025",
        "Natural Language Processing Course Project", "Python, NLP, viT5, Transformers, TextRank"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• Constructed a hybrid summarization engine combining extractive sentences filtering (TextRank with average Word2Vec embeddings) and abstractive transformer sequence generation (viT5-base).", style_bullet))
    story.append(Paragraph("• Conducted ablation studies analyzing the \"lost-in-the-middle\" effect on context lengths (512 vs 1024 tokens), proving that a 512-token input limit improves ROUGE-1 scores to 60.33 and ROUGE-L to 41.22 on 48,970 samples.", style_bullet))
    story.append(Spacer(1, 6))

    # Project 4
    story.append(create_item_header(
        "Containerized Hadoop Cluster &amp; Network Routing", "October, 2024",
        "Distributed Computing Research Project", "Hadoop 3.2.1, Docker, Docker Compose, Linux Networking"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• Deployed a distributed containerized HDFS cluster. Diagnosed and resolved NAT network issues preventing external hosts from reading/writing HDFS blocks due to DataNode dynamic container IP mapping.", style_bullet))
    story.append(Paragraph("• Implemented custom Docker bridge subnets, assigned static IP allocations (`172.22.0.2` and `172.22.0.3`), and mapped fixed hostnames in Docker files to allow external client connectivity.", style_bullet))
    story.append(Spacer(1, 6))

    # Project 5
    story.append(create_item_header(
        "Recyclable Waste Active Detection System", "October, 2025",
        "Computer Vision Course Term Paper", "YOLOv8, PyTorch, Active Learning, OpenCV"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• Created a real-time object detection model to identify six classes of recyclable waste (cardboard, glass, metal, paper, plastic, biodegradable) for robotic sorting lines.", style_bullet))
    story.append(Paragraph("• Designed a pool-based active learning loop utilizing least-confidence query strategies, increasing mAP50-95 from 0.0616 (Round 0) to 0.2131 (Round 3) with only 1,332 annotated images, decreasing labeling cost.", style_bullet))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # TECHNICAL SKILLS
    # ----------------------------------------------------
    story.extend(create_section_title("Technical Skills"))
    skills_data = [
      [Paragraph("<b>Languages</b>", style_item_title), Paragraph("Python, C++, Java, JavaScript, TypeScript, SQL (MySQL, PostgreSQL, SQLite)", style_body)],
      [Paragraph("<b>AI &amp; Data Science</b>", style_item_title), Paragraph("PyTorch, TensorFlow, Scikit-learn, Ultralytics YOLOv8, viT5, Hugging Face Transformers, Active Learning, OpenCV, Optuna, SHAP, LIME", style_body)],
      [Paragraph("<b>Web Engineering</b>", style_item_title), Paragraph("React.js, Next.js, Node.js, TailwindCSS, CSS Grid/Flexbox, Firebase, Vercel", style_body)],
      [Paragraph("<b>Tools &amp; Cloud</b>", style_item_title), Paragraph("Docker, Docker Compose, Linux/Ubuntu, Git, GitHub, Google Colab, WSL, WebHDFS", style_body)]
    ]
    t_skills = Table(skills_data, colWidths=[120, 403])
    t_skills.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 8))

    # Leadership & Extracurriculars
    story.extend(create_section_title("Leadership &amp; Extracurriculars"))
    story.append(create_item_header(
        "HUSC Chess Club &amp; Social Work Team", "2025 — Present",
        "Vice President (Chess Club) &amp; Volunteer", "Hue University, Vietnam"
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("• <b>Vice President of HUSC Chess Club:</b> Managed budget, scheduled matches, trained members, and co-hosted regional university championships. Awarded Certificate of Outstanding Leadership.", style_bullet))
    story.append(Paragraph("• <b>Social Work &amp; Volunteering:</b> Devoted 50+ hours in charity campaigns and faculty volunteering events (e.g. IT Chef, IT Talent campaigns) supporting community health and student engagement.", style_bullet))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # LANGUAGES
    # ----------------------------------------------------
    story.extend(create_section_title("Languages"))
    story.append(Paragraph("• <b>Vietnamese:</b> Native (Mother tongue).", style_bullet))
    story.append(Paragraph("• <b>English:</b> Professional Working Proficiency. British Council Aptis ESOL Certificate - CEFR B2.", style_bullet))
    story.append(Paragraph("• <b>Japanese:</b> Elementary / Beginner (N4/N5 currently studying).", style_bullet))
    story.append(Spacer(1, 8))

    # ----------------------------------------------------
    # RESEARCH INTERESTS
    # ----------------------------------------------------
    story.extend(create_section_title("Research Interests"))
    story.append(Paragraph("Computer Vision, Model Compression &amp; Quantization, Knowledge Distillation, Explainable AI (XAI), Natural Language Processing, Assistive &amp; Accessibility Tech (WCAG), Reinforcement Learning &amp; Wireless MAC Network Optimizations (RFID).", style_body))

    # Build Document
    doc.build(story)
    print(f"CV successfully generated and saved as '{filename}'!")

if __name__ == "__main__":
    build_pdf()
