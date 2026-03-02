import request from '@/utils/request'





// 查询用户推荐列表
export function listRecommendInfo(query) {
  return request({
    url: '/recruit/recommendInfo/list',
    method: 'get',
    params: query
  })
}

// 查询用户推荐详细
export function getRecommendInfo(id) {
  return request({
    url: '/recruit/recommendInfo/' +id,
    method: 'get'
  })
}

// 新增用户推荐
export function addRecommendInfo(data) {
  return request({
    url: '/recruit/recommendInfo',
    method: 'post',
    data: data
  })
}

// 修改用户推荐
export function updateRecommendInfo(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/recruit/recommendInfo',
    method: 'put',
    data: data
  })
}

// 删除用户推荐
export function delRecommendInfo(id) {
  return request({
    url: '/recruit/recommendInfo/' +id,
    method: 'delete'
  })
}