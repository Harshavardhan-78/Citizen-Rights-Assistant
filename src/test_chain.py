
from chains import ask_legal_assistant

query=[
      "I have recently brought land ,iam trying to develop it,but suddenly the community of that specific region trying to stop construction claiming that the land has suddendly emerged a god there we nned to built temple there what sould i do",
      "My neighbor threatened me. What rights do I have?","What is the punishment for causing hurt?","Can minorities establish educational institutions?",
      "What is theft according to IPC?","What is the Right to Equality?"]
res={q:ask_legal_assistant(q) for q in query}
for i,j in res.items():
    print(i)
    print(j)
    print("-"*150)