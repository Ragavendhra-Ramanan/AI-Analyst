from constants import PROJECT_ID, REGION
import vertexai


def init_vertex():
    vertexai.init(project=PROJECT_ID, location=REGION)
