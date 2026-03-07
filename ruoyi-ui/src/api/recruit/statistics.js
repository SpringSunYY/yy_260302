import request from '@/utils/request'

// 地图统计
export function mapStatistics(query) {
  return request({
    url: '/recruit/statistics/map',
    method: 'get',
    params: query
  })
}

//城市等级统计
export function cityLevelStatistics(query) {
  return request({
    url: '/recruit/statistics/cityLevel',
    method: 'get',
    params: query
  })
}

//岗位
export function postTypeStatistics(query) {
  return request({
    url: '/recruit/statistics/postType',
    method: 'get',
    params: query
  })
}

//学历
export function educationStatistics(query) {
  return request({
    url: '/recruit/statistics/education',
    method: 'get',
    params: query
  })
}

//企业规模
export function enterpriseSizeStatistics(query) {
  return request({
    url: '/recruit/statistics/enterpriseSize',
    method: 'get',
    params: query
  })
}

//经验
export function experienceStatistics(query) {
  return request({
    url: '/recruit/statistics/experience',
    method: 'get',
    params: query
  })
}
//主营业务
export function mainBusinessStatistics(query) {
  return request({
    url: '/recruit/statistics/mainBusiness',
    method: 'get',
    params: query
  })
}

//技能
export function skillStatistics(query) {
  return request({
    url: '/recruit/statistics/skill',
    method: 'get',
    params: query
  })
}

//工资
export function salaryStatistics(query) {
  return request({
    url: '/recruit/statistics/salary',
    method: 'get',
    params: query
  })
}

//融资情况
export function financingSituationStatistics(query) {
  return request({
    url: '/recruit/statistics/financingSituation',
    method: 'get',
    params: query
  })
}
