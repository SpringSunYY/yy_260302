import request from '@/utils/request'


// 查询招聘信息列表
export function listRecruitInfo(query) {
  return request({
    url: '/recruit/recruitInfo/list',
    method: 'get',
    params: query
  })
}

// 查询招聘信息详细
export function getRecruitInfo(recruitId) {
  return request({
    url: '/recruit/recruitInfo/' +recruitId,
    method: 'get'
  })
}
// 查询招聘信息详细
export function getRecruitInfoDetail(recruitId) {
  return request({
    url: '/recruit/recruitInfo/detail/' + recruitId,
    method: 'get'
  })
}

// 新增招聘信息
export function addRecruitInfo(data) {
  return request({
    url: '/recruit/recruitInfo',
    method: 'post',
    data: data
  })
}

// 修改招聘信息
export function updateRecruitInfo(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/recruit/recruitInfo',
    method: 'put',
    data: data
  })
}

// 删除招聘信息
export function delRecruitInfo(recruitId) {
  return request({
    url: '/recruit/recruitInfo/' +recruitId,
    method: 'delete'
  })
}

// 点赞或取消点赞
export function toggleLike(recruitId) {
  return request({
    url: '/recruit/likeInfo/like/' + recruitId,
    method: 'post'
  })
}
