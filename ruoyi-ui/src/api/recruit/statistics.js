import request from '@/utils/request'

export function mapStatistics(query){
  return request({
    url: '/recruit/statistics/map',
    method: 'get',
    params: query
  })
}
