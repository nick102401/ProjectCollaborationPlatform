import datetime

from FastApi.base.base_api import req_exec
from FastApi.base.common import Common
from FastApi.common.helper import month_switch, get_value_from_resp
from FastApi.conf import env


class ProjectMgt(Common):
    """
    项目概览
    """

    def __init__(self, headers={}, username=env.USERNAME, password=env.PASSWORD):
        super(ProjectMgt, self).__init__()
        self.page = 1
        self.pageSize = 15
        self.headers = headers
        self.username = username
        self.password = password

        # 请求头增加月份参数
        # 获取月份
        today = datetime.datetime.today()
        int_month = today.month
        month = month_switch(int_month)
        self.headers['team'] = month

    def get_project_list(self, keyword=''):
        """
        获取所有项目列表
        :param keyword: 关键字
        :return:
        """
        method = 'GET'
        url = '/api/project/getProjectList?page={0}&pageSize={1}&pjStatus=&keyword={2}'.format(self.page,
                                                                                               self.pageSize,
                                                                                               keyword)

        resp = req_exec(method, url, headers=self.headers, username=self.username, password=self.password)
        return resp

    def get_project_id_by_name(self, projectName):
        """
        根据项目名称获取项目ID
        :param projectName: 项目名称
        :return:
        """
        resp = self.get_project_list()
        projectId = get_value_from_resp(resp['content'], 'pid', 'name', projectName)
        return projectId

    def get_project_detail_by_name(self, projectName):
        """
        根据项目名称获取项目详情
        :param projectName: 项目名称
        :return:
        """
        projectId = self.get_project_id_by_name(projectName=projectName)

        method = 'GET'
        url = '/api/project/getProjectDetailById?pjId={0}&keyword='.format(projectId)

        resp = req_exec(method, url, headers=self.headers, username=self.username, password=self.password)
        return resp


if __name__ == '__main__':
    pm = ProjectMgt()
    # pm.get_project_list()
    # print(pm.get_project_id_by_name('演示系统'))
    # pm.get_project_detail_by_name('演示系统')
