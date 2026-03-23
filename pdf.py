# Create a PDF with ~200 words using reportlab

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("rag.pdf")
styles = getSampleStyleSheet()

text = """Cricket is one of the most popular sports in the world, especially in countries like India, Australia, England, and Pakistan. 
It is played between two teams of eleven players each on a circular or oval field with a rectangular pitch at the center. 
The game involves batting, bowling, and fielding, with the objective of scoring more runs than the opposing team.

There are three main formats of cricket: Test matches, One Day Internationals (ODIs), and Twenty20 (T20). Test cricket is the 
longest format, lasting up to five days, and is considered the most traditional form of the game. ODIs are limited to 50 overs 
per side, while T20 matches are the shortest, with 20 overs per team, making them fast-paced and highly entertaining.

Famous cricketers like Sachin Tendulkar, Virat Kohli, and Sir Donald Bradman have contributed significantly to the sport’s global 
popularity. Major tournaments such as the ICC Cricket World Cup and the Indian Premier League attract millions of viewers worldwide. 
Cricket is not just a sport but a passion for many fans, bringing people together and creating unforgettable moments."""

story = []
story.append(Paragraph(text, styles["Normal"]))
story.append(Spacer(1, 12))

doc.build(story)

"rag.pdf"