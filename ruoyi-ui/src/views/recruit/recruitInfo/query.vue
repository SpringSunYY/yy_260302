<template>
  <div class="app-container">
    <!-- 搜索栏 -->
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" label-width="80px" class="search-form">
      <el-form-item label="岗位大类" prop="postType">
        <el-select v-model="queryParams.postType" placeholder="请选择岗位大类" clearable>
          <el-option
            v-for="dict in dict.type.recruit_post_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="岗位" prop="post">
        <el-input
          v-model="queryParams.post"
          placeholder="请输入岗位"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="城市等级" prop="cityLevel">
        <el-select v-model="queryParams.cityLevel" placeholder="请选择城市等级" clearable>
          <el-option
            v-for="dict in dict.type.recruit_city_level"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="省份" prop="province">
        <el-input
          v-model="queryParams.province"
          placeholder="请输入省份"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="城市" prop="city">
        <el-input
          v-model="queryParams.city"
          placeholder="请输入城市"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="经验要求" prop="experienceRequired">
        <el-select v-model="queryParams.experienceRequired" placeholder="请选择经验要求" clearable>
          <el-option
            v-for="dict in dict.type.recruit_experience_required"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="学历要求" prop="educationRequired">
        <el-select v-model="queryParams.educationRequired" placeholder="请选择学历要求" clearable>
          <el-option
            v-for="dict in dict.type.recruit_education_required"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="技能要求" prop="skillRequired">
        <el-input
          v-model="queryParams.skillRequired"
          placeholder="请输入技能要求"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="企业名称" prop="enterpriseName">
        <el-input
          v-model="queryParams.enterpriseName"
          placeholder="请输入企业名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="主营业务" prop="mainBusiness">
        <el-input
          v-model="queryParams.mainBusiness"
          placeholder="请输入主营业务"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="企业规模" prop="enterpriseSize">
        <el-select v-model="queryParams.enterpriseSize" placeholder="请选择企业规模" clearable>
          <el-option
            v-for="dict in dict.type.recruit_enterprise_size"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="融资情况" prop="financingSituation">
        <el-select v-model="queryParams.financingSituation" placeholder="请选择融资情况" clearable>
          <el-option
            v-for="dict in dict.type.recruit_financing_situation"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 统计信息 -->
    <div class="total-info">
      <span class="total-text">共找到 <strong>{{ total }}</strong> 个岗位</span>
    </div>

    <!-- 卡片列表容器 -->
    <div
      class="card-container masonry-container"
      v-loading="loading"
    >
      <div class="masonry-wrapper">
        <div
          v-for="item in recruitList"
          :key="item.recruitId"
          class="masonry-item"
        >
          <el-card class="recruit-card" shadow="hover">
            <!-- 岗位标题 -->
            <div slot="header" class="card-header">
              <h3 class="post-title">{{ item.post || '未命名岗位' }}</h3>
            </div>

            <!-- 薪资信息 -->
            <div class="card-content">
              <div class="info-item salary">
                <i class="el-icon-coin"></i>
                <span class="label">薪资：</span>
                <span class="value highlight">{{ item.salaryRange || '面议' }}</span>
              </div>

              <!-- 地点 -->
              <div class="info-item">
                <i class="el-icon-location-outline"></i>
                <span class="label">地点：</span>
                <span class="value">{{ item.location || '未指定' }}</span>
              </div>

              <!-- 企业名称 -->
              <div class="info-item">
                <i class="el-icon-office-building"></i>
                <span class="label">企业：</span>
                <span class="value">{{ item.enterpriseName || '未指定' }}</span>
              </div>

              <!-- 经验要求 -->
              <div class="info-item" v-if="item.experienceRequired">
                <i class="el-icon-user"></i>
                <span class="label">经验：</span>
                <dict-tag :options="dict.type.recruit_experience_required" :value="item.experienceRequired"/>
              </div>

              <!-- 学历要求 -->
              <div class="info-item" v-if="item.educationRequired">
                <i class="el-icon-reading"></i>
                <span class="label">学历：</span>
                <dict-tag :options="dict.type.recruit_education_required" :value="item.educationRequired"/>
              </div>

              <!-- 企业规模 -->
              <div class="info-item" v-if="item.enterpriseSize">
                <i class="el-icon-s-data"></i>
                <span class="label">规模：</span>
                <dict-tag :options="dict.type.recruit_enterprise_size" :value="item.enterpriseSize"/>
              </div>

              <!-- 上市情况 -->
              <div class="info-item" v-if="item.listingStatus">
                <i class="el-icon-trophy"></i>
                <span class="label">上市：</span>
                <dict-tag :options="dict.type.recruit_listing_status" :value="item.listingStatus"/>
              </div>

              <!-- 技能要求 -->
              <div class="info-item skill" v-if="item.skillRequired">
                <i class="el-icon-star-on"></i>
                <span class="label">技能：</span>
                <span class="value skill-text">{{ item.skillRequired }}</span>
              </div>

              <!-- 标题链接 -->
              <div class="card-footer">
                <el-button
                  type="text"
                  icon="el-icon-view"
                  @click="openDetail(item)"
                  class="link-btn"
                >
                  查看详情
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 加载提示 -->
      <div class="load-more-tip" v-if="hasMore">
        <i class="el-icon-loading" v-if="loadingMore"></i>
        <span>{{ loadingMore ? '加载中...' : '滚动加载更多' }}</span>
      </div>
      <div class="load-more-tip no-more" v-if="!hasMore && recruitList.length > 0">
        <span>没有更多数据了</span>
      </div>
      <div class="empty-tip" v-if="!loading && recruitList.length === 0">
        <el-empty description="暂无数据"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
import { listRecruitInfo } from "@/api/recruit/recruitInfo";

export default {
  name: "RecruitInfoQuery",
  dicts: ['recruit_post_type', 'recruit_city_level', 'recruit_experience_required', 'recruit_education_required', 'recruit_enterprise_size', 'recruit_financing_situation'],
  data() {
    return {
      // 遮罩层
      loading: false,
      // 加载更多中
      loadingMore: false,
      // 招聘信息表表格数据
      recruitList: [],
      // 总条数
      total: 0,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        post: null,
        location: null,
        experienceRequired: null,
        educationRequired: null,
        skillRequired: null,
        enterpriseName: null,
        listingStatus: null,
        enterpriseSize: null,
        mainBusiness: null,
      },
      // 是否还有更多数据
      hasMore: true,
      // 滚动定时器
      scrollTimer: null
    };
  },
  computed: {
    // 是否禁用无限滚动
    disabled() {
      return this.loading || this.loadingMore || !this.hasMore;
    }
  },
  created() {
    this.getList();
  },
  mounted() {
    // 绑定窗口滚动事件
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    // 移除窗口滚动事件
    window.removeEventListener('scroll', this.handleScroll);
    // 清除定时器
    if (this.scrollTimer) {
      clearTimeout(this.scrollTimer);
    }
  },
  methods: {
    /** 查询招聘信息表列表 */
    getList(reset = false) {
      if (reset) {
        this.queryParams.pageNum = 1;
        this.recruitList = [];
        this.hasMore = true;
        this.loading = true;
      } else {
        this.loadingMore = true;
      }

      listRecruitInfo(this.queryParams).then(response => {
        if (reset) {
          this.recruitList = response.rows || [];
        } else {
          this.recruitList = [...this.recruitList, ...(response.rows || [])];
        }
        this.total = response.total || 0;

        // 判断是否还有更多数据
        this.hasMore = this.recruitList.length < this.total;

        this.loading = false;
        this.loadingMore = false;
      }).catch(() => {
        this.loading = false;
        this.loadingMore = false;
      });
    },
    /** 加载更多 */
    loadMore() {
      if (this.loading || this.loadingMore || !this.hasMore) {
        return;
      }

      this.loadingMore = true;
      this.queryParams.pageNum += 1;
      this.getList(false);
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.getList(true);
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.getList(true);
    },
    /** 打开详情页 */
    openDetail(row) {
      const route = this.$router.resolve({ name: 'RecruitInfoDetail', query: { recruitId: row.recruitId } })
      window.open(route.href, '_blank')
    },
    /** 打开链接 */
    openLink(url) {
      if (url) {
        this.openDetail({ recruitId: url })
      }
    },
    /** 处理滚动事件 - 使用节流优化性能 */
    handleScroll() {
      // 如果正在加载或没有更多数据，则不处理
      if (this.loading || this.loadingMore || !this.hasMore) {
        return;
      }

      // 节流处理，避免频繁触发
      if (this.scrollTimer) {
        clearTimeout(this.scrollTimer);
      }

      this.scrollTimer = setTimeout(() => {
        // 获取滚动位置
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const documentHeight = document.documentElement.scrollHeight || document.body.scrollHeight;

        // 当滚动到距离底部200px时加载更多
        if (scrollTop + windowHeight >= documentHeight - 200) {
          this.loadMore();
        }
      }, 100);
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.search-form {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.total-info {
  background: #fff;
  padding: 15px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .total-text {
    font-size: 14px;
    color: #606266;

    strong {
      color: #409eff;
      font-size: 18px;
      font-weight: 600;
      margin: 0 4px;
    }
  }
}

.card-container {
  min-height: 400px;
  padding: 10px 0;
}

.masonry-container {
  width: 100%;
}

.masonry-wrapper {
  column-count: 4;
  column-gap: 20px;
  column-fill: balance;

  @media (max-width: 1920px) {
    column-count: 4;
  }

  @media (max-width: 1440px) {
    column-count: 3;
  }

  @media (max-width: 1024px) {
    column-count: 2;
  }

  @media (max-width: 768px) {
    column-count: 1;
  }
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 20px;
  display: inline-block;
  width: 100%;
}

.recruit-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  border-radius: 8px;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }

  ::v-deep .el-card__header {
    padding: 15px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: none;
    flex-shrink: 0;
  }

  ::v-deep .el-card__body {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }
}

.card-header {
  .post-title {
    margin: 0;
    color: #fff;
    font-size: 18px;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    font-size: 14px;
    color: #606266;
    flex-shrink: 0;

    &:last-child {
      margin-bottom: 0;
    }

    i {
      margin-right: 8px;
      color: #909399;
      font-size: 16px;
      width: 18px;
      text-align: center;
    }

    .label {
      margin-right: 6px;
      color: #909399;
      min-width: 50px;
    }

    .value {
      flex: 1;
      color: #303133;
      word-break: break-all;

      &.highlight {
        color: #f56c6c;
        font-weight: 600;
        font-size: 16px;
      }
    }

    &.salary {
      padding-bottom: 12px;
      margin-bottom: 15px;
      border-bottom: 1px dashed #e4e7ed;
    }

    &.skill {
      .skill-text {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.5;
      }
    }
  }
}

.card-footer {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
  text-align: center;
  flex-shrink: 0;

  .link-btn {
    color: #409eff;
    font-size: 14px;

    &:hover {
      color: #66b1ff;
    }
  }
}

.load-more-tip {
  text-align: center;
  padding: 20px;
  color: #909399;
  font-size: 14px;

  i {
    margin-right: 8px;
    animation: rotating 2s linear infinite;
  }

  &.no-more {
    color: #c0c4cc;
  }
}

.empty-tip {
  padding: 60px 0;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .card-container {
    padding: 5px 0;
  }

  .card-col {
    margin-bottom: 15px;
  }

  .recruit-card {
    ::v-deep .el-card__body {
      padding: 15px;
    }
  }

  .card-content {
    .info-item {
      font-size: 13px;
      margin-bottom: 10px;
    }
  }
}
</style>

