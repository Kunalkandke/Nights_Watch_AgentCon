import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from medcompliance.agents.workflow import run_compliance_workflow
print("Import OK")
print("LangGraph available:", end=" ")
try:
    from langgraph.graph import StateGraph
    print("YES")
except:
    print("NO - will use sequential fallback")
