from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime
import random


def generate_pdf(
        student_name,
        essay_topic,
        result,
        filename):

    doc=SimpleDocTemplate(filename)

    doc.title="AI Essay Evaluation Report"
    doc.author=student_name
    doc.subject="Intelligent Essay Evaluation and Academic Performance Analytics System"

    styles=getSampleStyleSheet()

    content=[]

    try:

        logo=Image(
            "assets/logo.png",
            width=120,
            height=120
        )

        content.append(logo)

    except Exception:
        pass

    content.append(
        Paragraph(
            "KALINGA INSTITUTE OF INDUSTRIAL TECHNOLOGY",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "Intelligent Essay Evaluation and Academic Performance Analytics System",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,15)
    )

    report_id=(
        "REP-"+
        str(random.randint(1000,9999))
    )

    current_time=datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    content.append(
        Paragraph(
            f"<b>Report ID:</b> {report_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Date:</b> {current_time}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            "Student Information",
            styles["Heading2"]
        )
    )

    student_table=Table(
        [
            ["Student Name",student_name],
            ["Essay Topic",essay_topic],
            ["Essay Type",result["essay_type"]],
            ["Reading Time",f"{result['reading_time']} min"]
        ],
        colWidths=[140,260]
    )

    student_table.setStyle(
        TableStyle([

            ("GRID",
             (0,0),
             (-1,-1),
             1,
             colors.black),

            ("BACKGROUND",
             (0,0),
             (0,-1),
             colors.lightgrey),

            ("FONTNAME",
             (0,0),
             (0,-1),
             "Helvetica-Bold")

        ])
    )

    content.append(student_table)

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            "Evaluation Results",
            styles["Heading2"]
        )
    )

    score_table=Table(
        [

            ["Metric","Score"],

            ["Grammar Score",
             str(result["grammar_score"])],

            ["Vocabulary Score",
             str(result["vocabulary_score"])],

            ["Readability Score",
             str(result["readability_score"])],

            ["Grammar Errors",
             str(result["grammar_errors"])],

            ["Paragraph Count",
             str(result["paragraph_count"])],

            ["Average Sentence Length",
             str(result["avg_sentence_length"])],

            ["ML Score",
             str(result["ml_score"])],

            ["Topic Relevance",
             str(result["topic_score"])],

            ["Plagiarism %",
             str(result["plagiarism_score"])],

            ["Final Score",
             str(result["overall_score"])]

        ],
        colWidths=[240,120]
    )

    score_table.setStyle(
        TableStyle([

            ("GRID",
             (0,0),
             (-1,-1),
             1,
             colors.black),

            ("BACKGROUND",
             (0,0),
             (-1,0),
             colors.lightblue),

            ("FONTNAME",
             (0,0),
             (-1,0),
             "Helvetica-Bold"),

            ("ALIGN",
             (1,1),
             (1,-1),
             "CENTER")

        ])
    )

    content.append(score_table)

    content.append(
        Spacer(1,20)
    )

    final_score=result["overall_score"]

    if final_score>=90:
        grade="Outstanding"

    elif final_score>=80:
        grade="Excellent"

    elif final_score>=70:
        grade="Good"

    elif final_score>=60:
        grade="Average"

    else:
        grade="Needs Improvement"

    content.append(
        Paragraph(
            f"<b>Overall Performance:</b> {grade}",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1,15)
    )

    content.append(
        Paragraph(
            "Performance Summary",
            styles["Heading2"]
        )
    )

    if final_score>=90:

        summary="""
        The essay demonstrates excellent language usage,
        strong topic relevance, high readability and
        outstanding overall academic quality.
        """

    elif final_score>=80:

        summary="""
        The essay demonstrates strong writing skills
        with good structure, vocabulary and content
        relevance.
        """

    elif final_score>=70:

        summary="""
        The essay is well written with moderate areas
        that can be improved for better academic
        quality.
        """

    else:

        summary="""
        The essay requires improvements in grammar,
        readability, vocabulary usage and overall
        presentation.
        """

    content.append(
        Paragraph(
            summary,
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1,15)
    )

    content.append(
        Paragraph(
            "Strengths",
            styles["Heading2"]
        )
    )

    if len(result["strengths"])>0:

        for item in result["strengths"]:

            content.append(
                Paragraph(
                    f"✓ {item}",
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No major strengths detected.",
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            "Areas for Improvement",
            styles["Heading2"]
        )
    )

    if len(result["weaknesses"])>0:

        for item in result["weaknesses"]:

            content.append(
                Paragraph(
                    f"• {item}",
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No major weaknesses detected.",
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1,15)
    )

    content.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading2"]
        )
    )

    recommendations=[]

    if result["grammar_score"]<80:
        recommendations.append(
            "Focus on improving grammar and sentence structure."
        )

    if result["vocabulary_score"]<50:
        recommendations.append(
            "Use a wider range of vocabulary."
        )

    if result["readability_score"]<70:
        recommendations.append(
            "Use shorter and clearer sentences."
        )

    if result["plagiarism_score"]>30:
        recommendations.append(
            "Increase originality and avoid copied content."
        )

    if len(recommendations)==0:
        recommendations.append(
            "Maintain the current writing quality and continue practicing."
        )

    for item in recommendations:

        content.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1,15)
    )

    content.append(
        Paragraph(
            "AI Feedback",
            styles["Heading2"]
        )
    )

    for item in result["feedback"]:

        content.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            "------------------------------------------------------------",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Generated by Intelligent Essay Evaluation and Academic Performance Analytics System",
            styles["Italic"]
        )
    )

    content.append(
        Paragraph(
            "Department of Computer Science & Engineering",
            styles["Italic"]
        )
    )

    content.append(
        Paragraph(
            "KIIT University",
            styles["Italic"]
        )
    )

    doc.build(content)