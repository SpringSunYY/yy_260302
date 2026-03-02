import request from '@/utils/request'





// 查询用户点赞列表
export function listLikeInfo(query) {
  return request({
    url: '/recruit/likeInfo/list',
    method: 'get',
    params: query
  })
}

// 查询用户点赞详细
export function getLikeInfo(id) {
  return request({
    url: '/recruit/likeInfo/' +id,
    method: 'get'
  })
}

// 新增用户点赞
export function addLikeInfo(data) {
  return request({
    url: '/recruit/likeInfo',
    method: 'post',
    data: data
  })
}

// 修改用户点赞
export function updateLikeInfo(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/recruit/likeInfo',
    method: 'put',
    data: data
  })
}

// 删除用户点赞
export function delLikeInfo(id) {
  return request({
    url: '/recruit/likeInfo/' +id,
    method: 'delete'
  })
}