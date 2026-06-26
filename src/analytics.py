import plotly.express as px
import plotly.graph_objects as go


def create_score_distribution(df):

    fig=px.histogram(
        df,
        x="overall_score",
        nbins=15,
        title="Overall Score Distribution"
    )

    fig.update_layout(
        xaxis_title="Score",
        yaxis_title="Number of Essays"
    )

    return fig


def create_student_performance(df):

    fig=px.bar(
        df,
        x="student_name",
        y="overall_score",
        color="overall_score",
        title="Student Performance Comparison"
    )

    fig.update_layout(
        xaxis_title="Student",
        yaxis_title="Overall Score"
    )

    return fig


def create_metric_summary(df):

    metrics={

        "total_essays":len(df),

        "average_score":round(
            df["overall_score"].mean(),
            2
        ),

        "highest_score":round(
            df["overall_score"].max(),
            2
        ),

        "lowest_score":round(
            df["overall_score"].min(),
            2
        )
    }

    return metrics


def create_score_pie_chart(df):

    categories=[]

    for score in df["overall_score"]:

        if score>=85:
            categories.append("Excellent")

        elif score>=70:
            categories.append("Good")

        elif score>=50:
            categories.append("Average")

        else:
            categories.append("Needs Improvement")

    temp=df.copy()

    temp["category"]=categories

    fig=px.pie(
        temp,
        names="category",
        title="Performance Categories"
    )

    return fig


def create_plagiarism_chart(df):

    fig=px.scatter(
        df,
        x="plagiarism_score",
        y="overall_score",
        hover_data=["student_name"],
        title="Plagiarism vs Overall Score"
    )

    return fig


def create_top_students(df):

    top_df=df.sort_values(
        by="overall_score",
        ascending=False
    ).head(10)

    fig=px.bar(
        top_df,
        x="student_name",
        y="overall_score",
        title="Top Performing Students"
    )

    return fig