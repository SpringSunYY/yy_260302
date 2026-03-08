<template>
  <div class="app-container">
    <el-card class="detail-card" v-loading="loading">
      <!-- 头部信息 -->
      <div slot="header" class="clearfix">
        <div class="header-content">
          <div class="title-section">
            <h1 class="post-title">{{ recruitInfo.post || '未命名岗位' }}</h1>
            <div class="post-meta">
              <span class="meta-item" v-if="recruitInfo.postType">
                <i class="el-icon-collection"></i>
                <dict-tag :options="dict.type.recruit_post_type" :value="recruitInfo.postType"/>
              </span>
              <span class="meta-item" v-if="recruitInfo.postUpdateTime">
                <i class="el-icon-time"></i>
                {{ parseTime(recruitInfo.postUpdateTime, '{y}-{m}-{d}') }}
              </span>
            </div>
          </div>
          <div class="action-section" v-hasPermi="['recruit:likeInfo:add']">
            <el-button
              :type="recruitInfo.isLiked ? 'danger' : 'primary'"
              :icon="recruitInfo.isLiked ? 'el-icon-star-on' : 'el-icon-star-off'"
              @click="handleToggleLike"
              v-hasPermi="['recruit:likeInfo:add']"
              :loading="likeLoading"
            >
              {{ recruitInfo.isLiked ? '取消点赞' : '点赞' }}
            </el-button>
          </div>
        </div>
      </div>

      <!-- 薪资信息 -->
      <div class="section salary-section">
        <h3 class="section-title">
          <i class="el-icon-coin"></i>
          薪资待遇
        </h3>
        <div class="salary-content">
          <div class="salary-main">
            <span class="salary-range">{{ recruitInfo.salaryRange || '面议' }}</span>
            <span class="salary-avg" v-if="recruitInfo.salaryMonthAvg">
              (平均月薪: {{ recruitInfo.salaryMonthAvg.toFixed(2) }}K)
            </span>
          </div>
          <div class="salary-remark" v-if="recruitInfo.salaryRemark">
            {{ recruitInfo.salaryRemark }}
          </div>
          <div class="bonus-performance" v-if="recruitInfo.bonusPerformance">
            <span class="label">奖金绩效：</span>
            <span class="value">{{ recruitInfo.bonusPerformance }}</span>
          </div>
        </div>
      </div>

      <!-- 基本信息 -->
      <div class="section">
        <h3 class="section-title">
          <i class="el-icon-info"></i>
          基本信息
        </h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">工作地点：</span>
            <span class="value">{{ recruitInfo.location || recruitInfo.city || '未指定' }}</span>
          </div>
          <div class="info-item">
            <span class="label">省份/城市：</span>
            <span class="value">{{ recruitInfo.province || '' }} {{ recruitInfo.province && recruitInfo.city ? '/' : '' }} {{ recruitInfo.city || '' }}</span>
          </div>
          <div class="info-item">
            <span class="label">城市等级：</span>
            <span class="value">
              <dict-tag :options="dict.type.recruit_city_level" :value="recruitInfo.cityLevel"/>
            </span>
          </div>
          <div class="info-item">
            <span class="label">经验要求：</span>
            <span class="value">
              <dict-tag :options="dict.type.recruit_experience_required" :value="recruitInfo.experienceRequired"/>
            </span>
          </div>
          <div class="info-item">
            <span class="label">学历要求：</span>
            <span class="value">
              <dict-tag :options="dict.type.recruit_education_required" :value="recruitInfo.educationRequired"/>
            </span>
          </div>
          <div class="info-item" v-if="recruitInfo.skillRequired">
            <span class="label">技能要求：</span>
            <span class="value skill-text">{{ recruitInfo.skillRequired }}</span>
          </div>
        </div>
      </div>

      <!-- 企业信息 -->
      <div class="section">
        <h3 class="section-title">
          <i class="el-icon-office-building"></i>
          企业信息
        </h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">企业名称：</span>
            <span class="value enterprise-name">{{ recruitInfo.enterpriseName || '未指定' }}</span>
          </div>
          <div class="info-item">
            <span class="label">融资情况：</span>
            <span class="value">
              <dict-tag :options="dict.type.recruit_financing_situation" :value="recruitInfo.financingSituation"/>
            </span>
          </div>
          <div class="info-item" v-if="recruitInfo.mainBusiness">
            <span class="label">主营业务：</span>
            <span class="value">{{ recruitInfo.mainBusiness }}</span>
          </div>
          <div class="info-item">
            <span class="label">企业规模：</span>
            <span class="value">
              <dict-tag :options="dict.type.recruit_enterprise_size" :value="recruitInfo.enterpriseSize"/>
            </span>
          </div>
          <div class="info-item full-width" v-if="recruitInfo.enterpriseDesc">
            <span class="label">企业介绍：</span>
            <span class="value enterprise-desc">{{ recruitInfo.enterpriseDesc }}</span>
          </div>
        </div>
      </div>

      <!-- 岗位描述 -->
      <div class="section" v-if="recruitInfo.postDesc">
        <h3 class="section-title">
          <i class="el-icon-document"></i>
          岗位描述
        </h3>
        <div class="post-desc" v-html="recruitInfo.postDesc"></div>
      </div>

      <!-- 其他信息 -->
      <div class="section" v-if="recruitInfo.remark">
        <h3 class="section-title">
          <i class="el-icon-more"></i>
          备注
        </h3>
        <div class="remark">{{ recruitInfo.remark }}</div>
      </div>

      <!-- 底部操作 -->
      <div class="footer-actions">
        <el-button
          v-if="recruitInfo.titleUrl"
          type="primary"
          icon="el-icon-link"
          @click="openOriginalUrl"
        >
          查看原文
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getRecruitInfoDetail, toggleLike } from "@/api/recruit/recruitInfo";

export default {
  name: "RecruitInfoDetail",
  dicts: ['recruit_post_type', 'recruit_city_level', 'recruit_experience_required', 'recruit_education_required', 'recruit_enterprise_size', 'recruit_financing_situation'],
  data() {
    return {
      // 遮罩层
      loading: false,
      // 点赞加载中
      likeLoading: false,
      // 招聘信息详情
      recruitInfo: {
        isLiked: false
      }
    };
  },
  created() {
    const recruitId = this.$route.query.recruitId;
    if (recruitId) {
      this.getDetail(recruitId);
    }
  },
  methods: {
    /** 查询招聘信息详情 */
    getDetail(recruitId) {
      this.loading = true;
      getRecruitInfoDetail(recruitId).then(response => {
        this.recruitInfo = response.data || {};
        this.loading = false;
      }).catch(() => {
        this.loading = false;
      });
    },
    /** 点赞/取消点赞 */
    handleToggleLike() {
      if (!this.recruitInfo.recruitId) {
        return;
      }

      this.likeLoading = true;
      toggleLike(this.recruitInfo.recruitId).then(response => {
        this.likeLoading = false;
        if (response.code === 200) {
          // 更新点赞状态
          this.recruitInfo.isLiked = response.data.isLiked;
          this.$message.success(response.msg);
        }
      }).catch(() => {
        this.likeLoading = false;
      });
    },
    /** 打开原文链接 */
    openOriginalUrl() {
      if (this.recruitInfo.titleUrl) {
        window.open(this.recruitInfo.titleUrl, '_blank');
      }
    },
    /** 格式化时间 */
    parseTime(time, pattern) {
      if (!time) {
        return '';
      }
      const date = new Date(time);
      if (isNaN(date.getTime())) {
        return time;
      }
      const format = pattern || '{y}-{m}-{d}';
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return format.replace('{y}', year).replace('{m}', month).replace('{d}', day);
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.detail-card {
  width: 80%;
  margin: 0 auto;

  ::v-deep .el-card__header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
  }

  ::v-deep .el-card__body {
    padding: 30px;
  }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  color: #fff;
}

.title-section {
  flex: 1;
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 32px;
  font-weight: 700;
}

.post-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  opacity: 0.9;
}

.action-section {
  flex-shrink: 0;
}

.section {
  margin-bottom: 30px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #e4e7ed;

  i {
    color: #409eff;
  }
}

.salary-section {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
}

.salary-content {
  .salary-main {
    margin-bottom: 10px;
  }

  .salary-range {
    font-size: 28px;
    font-weight: 700;
    color: #f56c6c;
  }

  .salary-avg {
    font-size: 14px;
    color: #909399;
    margin-left: 10px;
  }

  .salary-remark {
    font-size: 14px;
    color: #606266;
    margin-bottom: 8px;
  }

  .bonus-performance {
    font-size: 14px;
    color: #606266;

    .label {
      font-weight: 500;
    }
  }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: flex-start;

  &.full-width {
    grid-column: 1 / -1;
  }

  .label {
    flex-shrink: 0;
    min-width: 80px;
    color: #909399;
    font-size: 14px;
  }

  .value {
    flex: 1;
    color: #303133;
    font-size: 14px;
    word-break: break-all;

    &.enterprise-name {
      font-weight: 600;
      font-size: 16px;
      color: #409eff;
    }

    &.enterprise-desc {
      line-height: 1.8;
    }

    &.skill-text {
      line-height: 1.6;
    }
  }
}

.post-desc {
  line-height: 1.8;
  color: #606266;
  font-size: 14px;
  white-space: pre-wrap;
}

.remark {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.footer-actions {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: center;
  gap: 15px;
}

// 响应式设计
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }

  .post-title {
    font-size: 20px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .detail-card {
    ::v-deep .el-card__body {
      padding: 15px;
    }
  }

  .salary-section {
    padding: 15px;
  }

  .salary-range {
    font-size: 24px !important;
  }
}
</style>
