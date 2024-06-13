from datetime import date

OPENAI_INITIAL_CONVERSATION = [
    {
        "role": "system",
        "content": "You are <Insert name>'s Resume Assistant. Make conversation sound natural, do not re-introduce yourself, always say <Insert name> has worked on or attribute to <Insert name>. You are a chat assistant LLM whose objective is to ingest the resume of <Insert name> and make conversation with the user to inform them about <Insert name>'s qualifications. Ensure responses are easy to understand and provide details and reasoning behind each response. For example, when providing context about <Insert name>'s experience, explain what they did at each job and why that makes them qualified. Keep responses concise when possible and format with markdown to make the text readable. Include direct references to the experiences, projects, and education provided to help show how <Insert name> is qualified. Note: Do not generate information outside of the context provided. Stick strongly to the experience, projects, education, and introduction given in the context provided! If you do not know the answer to a question, say that you do not know, and to contact <Insert name> directly using the email: <Insert email>. With each message, generate 3 suggested questions to 1) dive deeper into the current project or experience OR 2) Explore other similar/relevant projects and experience. You must respond in JSON format. The following is an example conversation you should model yourself after:",
    },
    {
        "role": "assistant",
        "content": """
{
    "message": "Hello! I am <Insert name>'s Resume Assistant! Feel free to ask me any questions about <Insert name>'s work experience, projects, education, and general qualifications. If you aren't sure what to ask, try these:\n",
    "suggestions": ["1. Give me a timeline of <Insert name>'s work experience.", "2. Tell me about <Insert name>'s experience with <Insert key resume topic>?", "3. Give me examples of <Insert name>'s leadership experience at <Insert key resume companies>."]
}
""",
    },
    {
        "role": "user",
        "content": "Hi! Can you give me some background into <Insert name>'s technical experience in <Insert field>?",
    },
    {
        "role": "assistant",
        "content": """
{
    "message": "Absolutely. <Insert name> has a total of X years of work experience in <Insert field>, spread across more than X different roles and X complex technical projects. Here is a summary of their most recent experience:

    1. **<Insert Job Title 1> at <Insert company 1>** (<Insert start date> to <Insert end date>)
    At <Insert company 1>, <Insert name> work across several teams and spearheaded the development of <Insert project>, working with <Insert technologies>, <Insert skills>, and achieving <Insert achievements>. This work had strong impact <Insert impact description here>.

    2. **<Insert Job Title 2> at <Insert company 2>** (<Insert start date> to <Insert end date>)
    At this position at <Insert company 2>, <Insert name> gained more experience with <Insert field> by <Insert project description>. They developed <Insert skills> over <Insert time>, which further qualifies them for <Insert position name>.

    Would you like to learn more about <Insert name>'s projects in the field?",
    "suggestions": ["Tell me more about <Insert name>'s experience at <Insert company 1>.", "Tell me more about <Insert name>'s experience at <Insert company 2>.", "What was the result of <Insert name>'s project at <Insert company 1>?"]
}
""",
    },
    {
        "role": "user",
        "content": """
Yes that would be very helpful. I am curious if <Insert name> has had experience working with <Insert technology>?
""",
    },
    {
        "role": "assistant",
        "content": """
{
    "message": "<Insert name> has actually worked on more than X projects using <Insert technology>, across the last <Insert time>. Here is a summary of the most notable projects:

    1. **<Insert Project Title 1>** (<Insert start date> to <Insert end date>)
    **Technologies/Skills: <Insert List of Technologies used>
    In <Insert Project Title 1>, <Insert name> implemented a <Insert project description> used by more than X users. <Insert name> utilized <Insert technology> to create <Insert project description>. 

    2. <Insert Project Title 2> (<Insert start date> to <Insert end date>)
    **Technologies/Skills**: <Insert List of Technologies used>
    <Insert Project Title 2> was another project that utilized <Insert technology>, which implemented a <Insert project description>. <Insert name> utilized <Insert technology> to create <Insert project description>.",
    "suggestions": ["Could you give me more details about <Insert Project Title 1>?", "Where can I find a link to <Insert Project Title 1>?", ", "Can you dive into the process of <Insert Project Title 2>?"]
}
""",
    },
    {
        "role": "user",
        "content": """
Could you give me more details about <Insert Project Title 1>?
""",
    },
    {
        "role": "assistant",
        "content": """
{
    "message": "Of course! <Insert Project Title 1> was a project that <Insert name> implemented between <Insert start> and <Insert end> with the purpose of <Insert project description>. <Insert more project details here>. For more details, please contact <Insert email> directly!",
    "suggestions": ["How can I collaborate with <Insert name> on this project?", "Where can I find this project?", "What are some of <Insert name>'s other similar projects and experiences?"]
}
""",
    },
]

SAMPLE_RESUME = {
    "intro": {
        "name": "Alex Zhu",
        "email": "alexanderzhu07@gmail.com",
        "summary": """
Hello! My name is Alex, and I am a third year student at Carnegie Mellon University studying Information Systems and Computer Science. I am particularly interested in working to solve large-scale problems within distributed systems and infrastructure, as well as cybersecurity.

As a student and engineer, I look forward to taking opportunities in fields or situations I am inexperienced or uncomfortable, especially those that give me the most room to grow and learn from those around me. I am keen to find experiences that challenge me to not only become a better developer, but a better communicator, leader, and teammate.

I highly prioritize learning and gaining experience on all parts of the tech stack, as well as in all facets as a developer. In the past, I have worked both as a technical leader and manager of a software development team at Studyfind, as well as cooperating and coordinating across several teams at Roblox to develop a new web pipeline.
""",
    },
    "experience": [
        {
            "title": "Founding Engineer",
            "company": "Mycelium Sports",
            "start": date(2024, 1, 1),
            "end": date(2024, 6, 3),
            "description": """
Co-led design and development efforts of two major initial prototypes used by 2 initial pilot users to process over 20 hours of sports content in less than 20 minutes each week. Rapidly deployed two prototypes in less than 1.5 weeks.

Created a backend utilizing AWS EC2 to host a computer vision algorithm using pose detection, face detection, and entropy-based analysis to find clips of interest, as well as AWS S3 to store videos and AWS DynamoDB to maintain metadata for user videos.            
""",
        },
        {
            "title": "15-210 Parallel Algorithms Teaching Assistant",
            "company": "Carnegie Mellon University",
            "start": date(2024, 1, 1),
            "end": date(2024, 5, 1),
            "description": """
Co-taught weekly 50-minute recitations on Parallel Algorithms topics including Trees, Randomized Algorithms, Graph Algorithms, and Dynamic Programming.

Hosted office hours for over 200 students to teach parallel algorithms proofs, code, and complexity analysis.        
""",
        },
        {
            "title": "App Infrastructure Software Engineer Intern",
            "company": "Roblox",
            "start": date(2023, 5, 1),
            "end": date(2023, 8, 1),
            "description": """
Conducted in-depth research and presented a proposal for a new development pipeline for the Roblox Web, utilizing web components. Successfully orchestrated a high-impact initiative that engaged more than 5 internal teams, showcasing a commitment to innovation and cross-functional collaboration.

Led the project as an App Infrastructure intern, steering crucial design decisions. Established a comprehensive framework for the Roblox Web pipeline by creating a GitHub template, publishing 3 npm packages, and developing 4 essential components. This end-to-end solution was integrated into the production environment, marking a significant milestone.

Through rigorous experimentation, confirmed the absence of negative effects on users or performance. Shared compelling findings with 3 stakeholder/early-adopter teams, preparing for pipeline integration into Roblox Web by Q1 of 2024
""",
        },
        {
            "title": "Lead Backend Engineer",
            "company": "Studyfind",
            "start": date(2023, 5, 1),
            "end": date(2024, 2, 1),
            "description": """     
Led and coordinated a dynamic team of 8 software developers, orchestrating Scrum sprints and implementing a streamlined workflow for design and development processes across the company.

Spearheaded the proposal and design of a MongoDB-based database system for the startup, integrating over 6 diverse datasets for efficient querying by HR, Marketing, and Software Engineering teams.

Oversaw the execution of 5 pivotal projects, including scraping and analyzing reviews from Yelp, automated emailing to clinical researchers, generating newsletters using ChatGPT, and outreach to Non-Profit organizations.
""",
        },
        {
            "title": "Software Developer",
            "company": "Studyfind",
            "start": date(2022, 12, 1),
            "end": date(2023, 5, 1),
            "description": """
Working as a part of the Business Intelligence team to automate file-processing and emailing to expand the registry of researchers at Studyfind to more than 200 researchers.

Led outreach to more than 20,000 clinical researchers through emailing campaigns and development of sentiment analysis for email responses.
""",
        },
        {
            "title": "Jr Software Developer Intern",
            "company": "Studyfind",
            "start": date(2022, 5, 1),
            "end": date(2022, 12, 1),
            "description": """
Created a cloud-docker application to further automate the emailing process and remove as much human interaction as possible from the process.

Created a file-processor library from scratch, that automates webscraping, splitting and emailing of files, and uploads, shares, and downloadeds files from Google Drive.

Worked as a part of the Business Intelligence team to create automated solutions, such as automating webscraping and outreach emailing of over 3000 researchers conducting research in underrepresented communities. 
""",
        },
    ],
    "projects": [
        {
            "title": "Ask My Resume",
            "organization": "Personal Project",
            "start": date(2024, 6, 1),
            "end": date(2024, 6, 3),
            "description": """
Created a chat interface for users to allow others to interact directly with their resume in a conversational manner. This seeks to address challenges with communication between founders, investors, recruiters, and engineers, to allow for each user to communicate and understand the background of another user without needing synchronous meeting times that are difficult to schedule.

Utilizes the OpenAI API and function-calling to implement the chat interface, prioritizes projects using AdaptKeyBERT for keyword ranking, and implements resume parsing for LinkedIn profiles.
""",
        },
        {
            "title": "Google Calendar Assistant",
            "organization": "Personal Project",
            "start": date(2024, 5, 26),
            "end": date(2025, 6, 3),
            "description": """
Developed and deployed a Python Streamlit application that creates a chat interface for users to schedule their daily events, which allows users to schedule their day in a conversational manner.

The application leverages the OpenAI API's function-calling and chat completion and the Google Calendar API to connect a chat assistant to the user's calendar and provide best-practices and suggestions for events.

In the process of deploying to users and developing a GoLang API and Google Extension using gRPC for full usage of an API for prospective users.
""",
        },
        {
            "title": "Distributed Bitcoin Miner",
            "organization": "Carnegie Mellon University",
            "start": date(2023, 10, 1),
            "end": date(2023, 11, 1),
            "description": """
Implemented an LSP communication protocol to provide reliable, in-order message passing within a client-server model across UDP connections using GoLang, sliding-window queues and priority heaps.

Distributed brute-force hash problems across multiple miners using a round-robin scheduling strategy to ensure fairness and efficiency for inputs of sizes scaling larger than 10^9, while tolerating miner and client failures on an unstable network.            
""",
        },
        {
            "title": "Deferrd (Startup)",
            "organization": "Deferrd",
            "start": date(2024, 1, 1),
            "end": date(2024, 4, 1),
            "description": """
Co-founded a startup dedicated to lowering barriers for starting companies, by utilizing Convertible Notes and SAFEs to mitigate the difficulties of hiring in early-stage startups without funding.

Actively engaged in developing an MVP using Amazon Web Services and NodeJS to manage backend communications, storage, and database operations, alongside a React frontend.
""",
        },
        {
            "title": "RAFT Consensus Algorithm",
            "organization": "Carnegie Mellon University",
            "start": date(2023, 11, 1),
            "end": date(2023, 12, 1),
            "description": """
Implemented the RAFT Consensus Algorithm to maintain consensus between groups of nodes, tolerating network partitions, failures, and inconsistencies.

Utilized GoLang to implement leader selection between groups of nodes, tolerating failed leader nodes and conflicts between multiple leader nodes. Maintained up-to-date logs at each node to allow for backtracking and failure tolerance, as well as consistency of new nodes in the network.

Facilitated concurrent communication between nodes using RPC calls to relay heartbeats, logs, and voting and term information.
""",
        },
    ],
    "education": [
        {
            "school": "Carnegie Mellon University",
            "degree": "B.S. in Information Systems with a Minor in Computer Science",
            "start": date(2021, 8, 1),
            "end": date(2025, 5, 1),
            "gpa": 4.0,
            "description": """
Relevant Coursework: 11-681 AI Venture Studio, 15-440 Distributed Systems, 15-213 Computer Systems, 15-210 Parallel and Sequential Algorithms, 67-262 Database Design and Development, 67-272 Application Design and Development.     
""",
        }
    ],
}
