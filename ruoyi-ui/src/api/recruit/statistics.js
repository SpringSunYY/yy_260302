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
