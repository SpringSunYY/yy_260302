<template>
  <div class="app-container">
    <div class="content-wrapper">
      <!-- 标题和信息左右布局 -->
      <div class="header-section">
        <!-- 标题在左 -->
        <h1 class="page-title">{{ modelInfo.algorithm }}</h1>

        <!-- 重新设计信息卡片，使用标签和数值分离的方式，更清晰美观 -->
        <div class="info-section">
          <div class="info-card">
            <div class="info-items">
              <div class="info-item">
                <span class="label">岗位</span>
                <span class="value">{{ weights.postType }}</span>
              </div>
              <div class="info-item">
                <span class="label">城市等级</span>
                <span class="value">{{ weights.cityLevel }}</span>
              </div>
              <div class="info-item">
                <span class="label">省份</span>
                <span class="value">{{ weights.province }}</span>
              </div>
              <div class="info-item">
                <span class="label">城市</span>
                <span class="value">{{ weights.city }}</span>
              </div>
              <div class="info-item">
                <span class="label">经验</span>
                <span class="value">{{ weights.experience }}</span>
              </div>
              <div class="info-item">
                <span class="label">学历</span>
                <span class="value">{{ weights.education }}</span>
              </div>
              <div class="info-item">
                <span class="label">主营业务</span>
                <span class="value">{{ weights.mainBusiness }}</span>
              </div>
              <div class="info-item">
                <span class="label">公司大小</span>
                <span class="value">{{ weights.enterpriseSize }}</span>
              </div>
              <div class="info-item">
                <span class="label">融资情况</span>
                <span class="value">{{ weights.financing }}</span>
              </div>
              <div class="info-item">
                <span class="label">工资</span>
                <span class="value">{{ weights.salary }}</span>
              </div>
              <div class="info-item">
                <span class="label">推荐数</span>
                <span class="value">{{ modelInfo.total }}</span>
              </div>
              <div class="info-item">
                <span class="label">时间衰减</span>
                <span class="value">{{ modelInfo.timeDecayFactor }}</span>
              </div>
              <div class="info-item">
                <span class="label">创建时间</span>
                <span class="value">{{ modelInfo.createTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <el-row :gutter="0" style="padding: 0">
        <el-col :xs="24" :sm="24" :lg="14">
          <div class="chart-wrapper">
            <PieLayerRateCharts
              :chart-title="postTypeModelName"
              :chart-data="postTypeModelData"
              @item-click="(item) => handleToQuery(item, 'postType')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="10">
          <div class="chart-wrapper">
            <PieGradientCharts
              :chart-data="cityLevelModelData"
              :chart-title="cityLevelModelName"
              @item-click="(item) => handleToQuery(item, 'cityLevel')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="10">
          <div class="chart-wrapper">
            <PiePetalPoseCharts
              :chart-data="provinceModelData"
              :chart-title="provinceModelName"
              @item-click="(item) => handleToQuery(item, 'province')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="14">
          <div class="chart-wrapper">
            <PieGradientRoseCharts
              :chart-data="cityModelData"
              :chart-title="cityModelName"
              @item-click="(item) => handleToQuery(item, 'city')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="14">
          <div class="chart-wrapper">
            <PiePetalTransparentPoseCharts
              :symbol-size="600"
              :chart-data="experienceModelData"
              :chart-title="experienceModelName"
              @item-click="(item) => handleToQuery(item, 'experienceRequired')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="10">
          <div class="chart-wrapper">
            <PiePetalTransparentPoseCharts
              :chart-data="educationModelData"
              :chart-title="educationModelName"
              @item-click="(item) => handleToQuery(item, 'educationRequired')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="14">
          <div class="chart-wrapper">
            <ScatterRandomTooltipCharts
              :chart-data="mainBusinessModelData"
              :chart-title="mainBusinessModelName"
              @item-click="(item) => handleToQuery(item, 'mainBusiness')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="10">
          <div class="chart-wrapper">
            <PieRoseLineCharts
              :chart-data="enterpriseSizeModelData"
              :chart-title="enterpriseSizeModelName"
              @item-click="(item) => handleToQuery(item, 'enterpriseSize')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="10">
          <div class="chart-wrapper">
            <PieRoundCharts
              :chart-data="financingModelData"
              :chart-title="financingModelName"
              @item-click="(item) => handleToQuery(item, 'financingSituation')"/>
          </div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="14">
          <div class="chart-wrapper">
            <PieGhostingCharts
              :chart-data="salaryModelData"
              :chart-title="salaryModelName"
            />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>

import {getRecommendInfo} from "@/api/recruit/recommendInfo";
import PiePetalTransparentPoseCharts from "@/components/Echarts/PiePetalTransparentPoseCharts.vue";
import PieGradientCharts from "@/components/Echarts/PieGradientCharts.vue";
import PiePetalPoseCharts from "@/components/Echarts/PiePetalPoseCharts.vue";
import PieGradientRoseCharts from "@/components/Echarts/PieGradientRoseCharts.vue";
import KeywordGravityCharts from "@/components/Echarts/KeywordGravityCharts.vue";
import StarsBorderBg from "@/components/BorderBg/StarsBorderBg.vue";
import PieLayerRateCharts from "@/components/Echarts/PieLayerRateCharts.vue";
import PieRoseHollowCharts from "@/components/Echarts/PieRoseHollowCharts.vue";
import PieRoseLineCharts from "@/components/Echarts/PieRoseLineCharts.vue";
import PieRoundCharts from "@/components/Echarts/PieRoundCharts.vue";
import PieGhostingCharts from "@/components/Echarts/PieGhostingCharts.vue";
import ScatterRandomTooltipCharts from "@/components/Echarts/ScatterRandomTooltipCharts.vue";


export default {
  name: "RecommendModel",
  components: {
    ScatterRandomTooltipCharts,
    PieGhostingCharts,
    PieRoundCharts,
    PieRoseLineCharts,
    PieRoseHollowCharts,
    PieLayerRateCharts,
    StarsBorderBg,
    KeywordGravityCharts,
    PieGradientRoseCharts,
    PiePetalPoseCharts,
    PieGradientCharts,
    PiePetalTransparentPoseCharts,
  },
  data() {
    return {
      recommend: {},
      recommendId: null,

      modelInfo: {},
      weights: {},
      //岗位
      postTypeModelData: [],
      postTypeModelName: '岗位推荐',
      //城市等级
      cityLevelModelData: [],
      cityLevelModelName: '城市等级',
      //省份
      provinceModelData: [],
      provinceModelName: '省份',
      //城市
      cityModelData: [],
      cityModelName: '城市',
      //经验
      experienceModelData: [],
      experienceModelName: '经验',
      //学历
      educationModelData: [],
      educationModelName: '学历',
      //主营业务
      mainBusinessModelData: [],
      mainBusinessModelName: '主营业务',
      //公司大小
      enterpriseSizeModelData: [],
      enterpriseSizeModelName: '公司大小',
      //融资情况
      financingModelData: [],
      financingModelName: '融资情况',
      //工资
      salaryModelData: [],
      salaryModelName: '工资',
    };
  },
  created() {
    this.id = this.$route.query.id;
    if (this.id) {
      this.getRecommendModel();
    }
  },
  methods: {
    getRecommendModel() {
      getRecommendInfo(this.id).then((response) => {
        this.recommend = response.data;
        let modelInfo = {}
        if (this.recommend.modelInfo) {
          modelInfo = JSON.parse(this.recommend.modelInfo)
          this.modelInfo = modelInfo
          this.weights = modelInfo.weights
        }
        let model = {}
        if (modelInfo.model) {
          model = modelInfo.model
        }
        if (model.postTypeModel) {
          this.postTypeModelData = model.postTypeModel
        }
        if (model.cityLevelModel) {
          this.cityLevelModelData = model.cityLevelModel
        }
        if (model.provinceModel) {
          this.provinceModelData = model.provinceModel
        }
        if (model.cityModel) {
          this.cityModelData = model.cityModel
        }
        if (model.experienceModel) {
          this.experienceModelData = model.experienceModel
        }
        if (model.educationModel) {
          this.educationModelData = model.educationModel
        }
        if (model.mainBusinessModel) {
          this.mainBusinessModelData = model.mainBusinessModel
        }
        if (model.enterpriseSizeModel) {
          this.enterpriseSizeModelData = model.enterpriseSizeModel
        }
        if (model.financingModel) {
          this.financingModelData = model.financingModel
        }
        if (model.salaryModel) {
          this.salaryModelData = model.salaryModel
        }
      });
    },
    handleToQuery(item, type) {
      if (item && item.name) {
        const routeData = this.$router.resolve({
          name: 'RecruitInfoQuery',
          query: {key: item.name, type: type}
        });
        window.open(routeData.href, '_blank');
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  background-image: url("../../../assets/images/map.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  padding: 32px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
}

.header-section {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 24px;
}

/* 标题居中，简洁大方 */
.page-title {
  flex: 2;
  font-size: 42px;
  font-weight: 700;
  color: #ffffff;
  padding-top: 10px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin: 0;
  text-align: center;
}

.info-section {
  flex: 4;
  display: flex;
  gap: 24px;
}

/* 重新设计卡片样式，使用清晰的标签和数值分离布局 */
.info-card {
  flex: 1;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.info-items {
  display: flex;
  padding: 20px 24px;
  gap: 28px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 20px;
  color: #ffffff;
  font-weight: 600;
}


.chart-wrapper {
  height: 40vh;
}

@media (max-width: 768px) {
  .app-container {
    padding: 20px;
  }

  .header-section {
    flex-direction: column;
    gap: 16px;
  }

  .page-title {
    text-align: center;
    margin-bottom: 16px;
  }

  .info-section {
    flex-direction: column;
  }

}
</style>
