import request from '@/utils/request'





// 查询用户浏览列表
export function listViewInfo(query) {
  return request({
    url: '/recruit/viewInfo/list',
    method: 'get',
    params: query
  })
}

// 查询用户浏览详细
export function getViewInfo(id) {
  return request({
    url: '/recruit/viewInfo/' +id,
    method: 'get'
  })
}

// 新增用户浏览
export function addViewInfo(data) {
  return request({
    url: '/recruit/viewInfo',
    method: 'post',
    data: data
  })
}

// 修改用户浏览
export function updateViewInfo(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/recruit/viewInfo',
    method: 'put',
    data: data
  })
}

// 删除用户浏览
export function delViewInfo(id) {
  return request({
    url: '/recruit/viewInfo/' +id,
    method: 'delete'
  })
}