import time

from FastApi.aws.project_mgt.project_detail import ProjectMgt
from FastApi.base.base_api import req_exec
from FastApi.common.helper import get_value_from_resp


class ProjectPlan(ProjectMgt):
    """
    项目计划
    """

    def __init__(self, projectName):
        super(ProjectPlan, self).__init__()
        self.projectName = projectName
        self.projectId = self.get_project_id_by_name(projectName=projectName)
        self.currentTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def create_project_plan(self, planTitle, startTime='', endTime='', remark='', leader=''):
        """
        创建项目计划
        :param planTitle: 项目计划名称
        :param startTime: 项目计划开始时间,默认为系统当前日期 %Y-%m-%d
        :param endTime: 项目计划结束时间,默认为系统当前日期 %Y-%m-%d
        :param remark: 描述
        :param leader: 负责人: 默认为当前用户
        :return:
        """
        if not leader:
            leader = self.username
        if not startTime:
            startTime = self.currentTime
        if not endTime:
            endTime = self.currentTime

        method = 'POST'
        url = '/api/project/updateProjecPlan'
        data = {
            "title": planTitle,
            "workType": "plan",
            "remark": remark,
            "startTime": startTime,
            "endTime": endTime,
            "leader": leader,
            "createPerson": self.username,
            "pid": self.projectId,
            "id": "",
            "status": "progress"
        }

        resp = req_exec(method, url, data=data, headers=self.headers, username=self.username, password=self.password)
        return resp

    def get_project_plans(self):
        """
        获取当前项目所有项目计划
        :return:
        """
        projectId = self.get_project_id_by_name(projectName=self.projectName)

        method = 'GET'
        url = '/api/project/getProjectPlan?pjId={0}'.format(projectId)

        resp = req_exec(method, url, headers=self.headers, username=self.username, password=self.password)
        return resp

    def get_project_plan_id_by_title(self, planTitle):
        """
        根据项目计划名称获取项目计划ID
        :param planTitle: 项目计划名称
        :return:
        """
        resp = self.get_project_plans()
        planId = get_value_from_resp(resp['content'], 'id', 'title', planTitle)

        method = 'GET'
        url = '/api/project/getPjItemDetail?pjItemId={0}&workType=plan'.format(planId)

        resp = req_exec(method, url, headers=self.headers, username=self.username, password=self.password)
        return resp


if __name__ == '__main__':
    pp = ProjectPlan('演示系统')
    pp.create_project_plan(planTitle='test_plan')
    # pp.get_project_plans()
    # pp.get_project_plan_id_by_title('test-mils', projectName='演示系统')
