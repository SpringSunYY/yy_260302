<template>
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

      <!-- 融资情况 -->
      <div class="info-item" v-if="item.financingSituation">
        <i class="el-icon-trophy"></i>
        <span class="label">融资：</span>
        <dict-tag :options="dict.type.recruit_financing_situation" :value="item.financingSituation"/>
      </div>

      <!-- 技能要求 -->
      <div class="info-item skill" v-if="item.skillRequired">
        <i class="el-icon-star-on"></i>
        <span class="label">技能：</span>
        <span class="value skill-text">{{ item.skillRequired }}</span>
      </div>

      <!-- 卡片底部 -->
      <div class="card-footer">
        <el-button
          type="text"
          icon="el-icon-view"
          @click="openDetail"
          class="link-btn"
        >
          查看详情
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'RecruitCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  dicts: ['recruit_experience_required', 'recruit_education_required', 'recruit_enterprise_size', 'recruit_financing_situation'],
  methods: {
    openDetail() {
      const route = this.$router.resolve({
        name: 'RecruitInfoDetail',
        query: { recruitId: this.item.recruitId }
      })
      window.open(route.href, '_blank')
    }
  }
}
</script>

<style lang="scss" scoped>
.recruit-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  border-radius: 8px;
  margin-bottom: 20px;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }

  ::v-deep .el-card__header {
    padding: 15px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    flex-shrink: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  ::v-deep .el-card__body {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;

  .post-title {
    margin: 0;
    color: #fff;
    font-size: 18px;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }

  .similarity-score {
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    margin-left: 10px;
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
</style>
