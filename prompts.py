def PromptActor():
    return """Act as an expert investment banker.
        {response}
        Context: '''{context}'''
        Question: '''{question}'''
        Answer: """

def PromptQuestions():
    questions = []

    questions.append("Provide a brief overview of the company's revenue and expenses.")
    questions.append("What was the key profitability ratios per year: Gross Profit Margin, Operating Profit Margin, Net Profit Margin")
    questions.append("Analyze trends in revenue and expenses over the past year.")

    # No information in the context for this?
    # questions.append("Assess the company's ability to generate consistent profits.")
    
    questions.append("Summarize the company's assets, liabilities, and equity.")
    questions.append("Calculate and discuss key liquidity and solvency ratios: Current Ratio, Quick Ratio, Debt-to-Equity Ratio")
    questions.append("Evaluate the company's financial stability and its ability to meet short-term and long-term obligations.")
    questions.append("Outline the company's operating, investing, and financing cash flows.")
    questions.append("Calculate and discuss the company's Free Cash Flow.")
    questions.append("Assess the company's cash flow generation and utilization.")
    questions.append("Calculate and interpret relevant financial ratios: Return on Assets (ROA), Return on Equity (ROE), Earnings Per Share (EPS), Price-Earnings (P/E) Ratio")
    
    # There's no information in the documents for this. Web search for benchmarks and historical data is needed
    # questions.append("Compare these ratios with industry benchmarks or historical data.")

    questions.append("Analyze trends in key financial metrics over multiple periods.")
    questions.append("Identify any significant changes or patterns and explain their implications.")
    questions.append("Compare the company's financial performance with its competitors or industry averages.")
    questions.append("Highlight strengths and weaknesses in comparison to peers.")
    questions.append("Identify potential financial risks based on the analysis.")
    questions.append("Discuss how the company manages or mitigates these risks.")
    questions.append("Summarize your overall assessment of the company's financial health and performance.")
    questions.append("Offer insights into areas of concern and areas of strength.")

    return questions

def PromptAnswerSetup():
    return """Answer the question below using the information in the Context.
        When answering with monetary values make sure the numbers are formatted as the correct currency.
        Do not explain how the answer is calculated, just give me the answer.
        Stop completion when the question is answered.
        Use linebreaks to nicely format the answer."""
