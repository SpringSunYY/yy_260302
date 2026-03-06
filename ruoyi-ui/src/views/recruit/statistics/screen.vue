<template>
  <div class="app-container">
    <el-row :gutter="0" style="padding: 0">
      <el-col :xs="24" :sm="24" :lg="6">
        <div class="chart-wrapper">
          <PieGradientCharts
            :chart-data="cityLevelStatisticsData"
            :chart-title="cityLevelStatisticsName"
            :label-show-value="false"
            @item-click="(item) => handleToQuery(item, 'cityLevel')"
          />
        </div>
        <div class="chart-wrapper">
          <PieLayerRateCharts
            :chart-data="postTypeStatisticsData"
            :chart-title="postTypeStatisticsName"
            @item-click="(item) => handleToQuery(item, 'postType')"/>
        </div>
        <div class="chart-wrapper">
          <PieRoseLineCharts
            :chart-data="enterpriseSizeStatisticsData"
            :chart-title="enterpriseSizeStatisticsName"
            @item-click="(item) => handleToQuery(item, 'enterpriseSize')"
          />
        </div>
        <div class="chart-wrapper">
          <div class="chart-wrapper">
            <PieGhostingCharts
              :chart-data="salaryStatisticsData"
              :chart-title="salaryStatisticsName"
              @item-click="(item) => handleToQuery(item, 'salary')"
            />
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <div class="map-chart-wrapper">
          <MapCharts
            :chart-data="mapStatisticsData"
            :chart-name="mapStatisticsName"
            default-index-name="岗位数"
            :summary-index-names="['岗位数']"
            @clickRegion="getMapData"
          />
        </div>
        <div class="expert-chart-wrapper">
          <ScatterRandomTooltipCharts
            :chart-title="mainBusinessStatisticsName"
            :chart-data="mainBusinessStatisticsData"
            @item-click="(item) => handleToQuery(item, 'mainBusiness')"
          />
        </div>
        <div class="center-chart-wrapper">
          <KeywordGravityCharts
            :font-size-range="[12,36]"
            :chart-data="skillStatisticsData"
            :chart-name="skillStatisticsName"
            @item-click="(item) => handleToQuery(item, 'skill')"/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="6">
        <div class="query-chart-wrapper">
          <LabelValueGrid
            @reset="reset"
            :data-list="tableQueryList"/>
        </div>
        <div class="chart-wrapper">
          <PiePetalTransparentPoseCharts
            :chart-data="educationStatisticsData"
            :chart-title="educationStatisticsName"
            @item-click="(item) => handleToQuery(item, 'education')"/>
        </div>
        <div class="rank-chart-wrapper">
          <PiePetalTransparentPoseCharts
            :label-show-value="false"
            :chart-data="experienceStatisticsData"
            :chart-title="experienceStatisticsName"
            @item-click="(item) => handleToQuery(item, 'experience')"/>
        </div>
        <div class="chart-wrapper">

        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import KeywordGravityCharts from "@/components/Echarts/KeywordGravityCharts.vue";
import MapCharts from "@/components/Echarts/MapCharts.vue";
import PieGradientCharts from "@/components/Echarts/PieGradientCharts.vue";
import ScatterRandomTooltipCharts from "@/components/Echarts/ScatterRandomCharts.vue";
import PiePetalPoseCharts from "@/components/Echarts/PiePetalPoseCharts.vue";
import PiePetalTransparentPoseCharts from "@/components/Echarts/PiePetalTransparentPoseCharts.vue";
import PieGradientRoseCharts from "@/components/Echarts/PieGradientRoseCharts.vue";
import BarRankingZoomCharts from "@/components/Echarts/BarRankingZoomCharts.vue";
import BarLineZoomCharts from "@/components/Echarts/BarLineZoomCharts.vue";
import TableRanking from "@/components/Echarts/TableRanking.vue";
import LabelValueGrid from "@/components/Echarts/LabelValueList.vue";
import {
  cityLevelStatistics,
  educationStatistics,
  enterpriseSizeStatistics,
  experienceStatistics,
  mainBusinessStatistics,
  mapStatistics,
  postTypeStatistics,
  salaryStatistics,
  skillStatistics
} from "@/api/recruit/statistics";
import PieLayerRateCharts from "@/components/Echarts/PieLayerRateCharts.vue";
import PieRoseLineCharts from "@/components/Echarts/PieRoseLineCharts.vue";
import PieGhostingCharts from "@/components/Echarts/PieGhostingCharts.vue";

const baseQuery = [
  {
    label: '地区',
    value: '全国',
    key: 'address',
  },
  {
    label: '城市等级',
    value: '全部',
    key: 'cityLevel',
  },
  {
    label: '岗位',
    value: '全部',
    key: 'postType',
  },
  {
    label: '学历',
    value: '全部',
    key: 'education',
  },
  {
    label: '企业规模',
    value: '全部',
    key: 'enterpriseSize',
  },
  {
    label: '经验',
    value: '全部',
    key: 'experience',
  },
  {
    label: '主营业务',
    value: '全部',
    key: 'mainBusiness',
  },
  {
    label: '技能',
    value: '全部',
    key: 'skill',
  },
  {
    label: '工资',
    value: '全部',
    key: 'salary',
  }
]

export default {
  name: "SalesStatisticsScreen",
  components: {
    PieGhostingCharts,
    PieRoseLineCharts,
    PieLayerRateCharts,
    LabelValueGrid,
    TableRanking,
    BarLineZoomCharts,
    BarRankingZoomCharts,
    PieGradientRoseCharts,
    PiePetalTransparentPoseCharts,
    PiePetalPoseCharts, ScatterRandomTooltipCharts, PieGradientCharts, MapCharts, KeywordGravityCharts
  },
  directives: {
    lazy: {
      inserted(el) {
        // 使用 Intersection Observer 实现懒加载
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target;
              // 加载真实图片
              if (img.dataset.src) {
                img.src = img.dataset.src;
              }
              img.classList.add('lazy-loaded');
              observer.unobserve(img);
            }
          });
        }, {
          rootMargin: '50px', // 提前 50px 开始加载
          threshold: 0.1
        });
        observer.observe(el);
      }
    }
  },
  data() {
    return {
      query: {},
      tableQueryList: baseQuery,
      tableColumns: [
        {label: '封面', prop: 'coverImage', show: false},
        {label: '系列', prop: 'name'},
        {label: '速度', prop: 'value'}
      ],
      //工资地图
      mapStatisticsData: [],
      mapStatisticsName: "工资地图",
      //城市等级
      cityLevelStatisticsData: [],
      cityLevelStatisticsName: "城市等级分析",
      cityLevelStatisticsNameOrigin: "城市等级分析",
      //岗位
      postTypeStatisticsData: [],
      postTypeStatisticsName: "岗位分析",
      postTypeStatisticsNameOrigin: "岗位分析",
      //学历
      educationStatisticsData: [],
      educationStatisticsName: "学历分析",
      educationStatisticsNameOrigin: "学历分析",
      //企业规模
      enterpriseSizeStatisticsData: [],
      enterpriseSizeStatisticsName: "企业规模分析",
      enterpriseSizeStatisticsNameOrigin: "企业规模分析",
      //经验
      experienceStatisticsData: [],
      experienceStatisticsName: "经验分析",
      experienceStatisticsNameOrigin: "经验分析",
      //主营业务
      mainBusinessStatisticsData: [],
      mainBusinessStatisticsName: "主营业务分析",
      mainBusinessStatisticsNameOrigin: "主营业务分析",
      //技能
      skillStatisticsData: [],
      skillStatisticsName: "技能分析",
      skillStatisticsNameOrigin: "技能分析",
      //工资
      salaryStatisticsData: [],
      salaryStatisticsName: "工资分析",
      salaryStatisticsNameOrigin: "工资分析",
    }
  },
  created() {
    this.getStatisticsData()
  },
  methods: {
    getMapData(data) {
      if (!data.canDrillDown && !data.isBack) return
      this.query.address = data.name
      let addressName = data.name
      if (addressName === '中华人民共和国') {
        addressName = '中国'
      }
      //如果包含省、自治区，去除
      if (addressName.includes('省')) {
        addressName = addressName.replace('省', '')
      }
      if (addressName.includes('壮族自治区')) {
        addressName = addressName.replace('壮族自治区', '')
      }
      if (addressName.includes('维吾尔自治区')) {
        addressName = addressName.replace('维吾尔自治区', '')
      }
      if (addressName.includes('自治区')) {
        addressName = addressName.replace('自治区', '')
      }
      if (addressName.includes('市')) {
        addressName = addressName.replace('市', '')
      }
      this.resetLabelQuery('address', addressName)
      this.cityLevelStatisticsName = addressName + '-' + this.cityLevelStatisticsNameOrigin
      this.postTypeStatisticsName = addressName + '-' + this.postTypeStatisticsNameOrigin
      this.educationStatisticsName = addressName + '-' + this.educationStatisticsNameOrigin
      this.enterpriseSizeStatisticsName = addressName + '-' + this.enterpriseSizeStatisticsNameOrigin
      this.experienceStatisticsName = addressName + '-' + this.experienceStatisticsNameOrigin
      this.mainBusinessStatisticsName = addressName + '-' + this.mainBusinessStatisticsNameOrigin
      this.skillStatisticsName = addressName + '-' + this.skillStatisticsNameOrigin
      this.salaryStatisticsName = addressName + '-' + this.salaryStatisticsNameOrigin
      this.getStatisticsData()
    },
    getStatisticsData() {
      this.getMapStatisticsData()
      this.getCityLevelStatisticsData()
      this.getPostTypeStatisticsData()
      this.getEducationStatisticsData()
      this.getEnterpriseSizeStatisticsData()
      this.getExperienceStatisticsData()
      this.getMainBusinessStatisticsData()
      this.getSkillStatisticsData()
      this.getSalaryStatisticsData()
    },
    getMapStatisticsData() {
      mapStatistics(this.query).then(res => {
        if (!res.data) return
        //构建结果
        this.mapStatisticsData = []
        //岗位数、平均工资、最高工资、最低工资
        let postNum = []
        let avgSalary = []
        let maxSalary = []
        let minSalary = []
        for (let i = 0; i < res.data.length; i++) {
          const item = res.data[i]
          const name = item.name
          postNum.push({
            location: name,
            value: item.value
          })
          avgSalary.push({
            location: name,
            value: item.avg
          })
          maxSalary.push({
            location: name,
            value: item.max
          })
          minSalary.push({
            location: name,
            value: item.min
          })
        }
        this.mapStatisticsData.push(
          {
            name: '岗位数',
            value: postNum
          },
          {
            name: '平均工资',
            value: avgSalary
          },
          {
            name: '最高工资',
            value: maxSalary
          },
          {
            name: '最低工资',
            value: minSalary
          }
        )
      })
    },
    //城市等级
    getCityLevelStatisticsData() {
      cityLevelStatistics({
        ...this.query,
        cityLevel: null
      }).then(res => {
        if (!res.data) return
        this.cityLevelStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.cityLevelStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //岗位
    getPostTypeStatisticsData() {
      postTypeStatistics({
        ...this.query,
        postType: null
      }).then(res => {
        if (!res.data) return
        this.postTypeStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.postTypeStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //学历
    getEducationStatisticsData() {
      educationStatistics({
        ...this.query,
        education: null
      }).then(res => {
        if (!res.data) return
        this.educationStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.educationStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //企业规模
    getEnterpriseSizeStatisticsData() {
      enterpriseSizeStatistics({
        ...this.query,
        enterpriseSize: null
      }).then(res => {
        if (!res.data) return
        this.enterpriseSizeStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.enterpriseSizeStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //经验
    getExperienceStatisticsData() {
      experienceStatistics({
        ...this.query,
        experience: null
      }).then(res => {
        if (!res.data) return
        this.experienceStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.experienceStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //主营业务
    getMainBusinessStatisticsData() {
      mainBusinessStatistics({
        ...this.query,
        mainBusiness: null
      }).then(res => {
        if (!res.data) return
        this.mainBusinessStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.mainBusinessStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //技能
    getSkillStatisticsData() {
      skillStatistics({
        ...this.query,
        skill: null
      }).then(res => {
        if (!res.data) return
        this.skillStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.skillStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    //工资
    getSalaryStatisticsData() {
      salaryStatistics({
        ...this.query,
        maxSalary: null,
        minSalary: null
      }).then(res => {
        if (!res.data) return
        this.salaryStatisticsData = []
        res.data.forEach(item => {
          const tooltipText =
            `平均工资：${item.avg}<br>` +
            `最高工资：${item.max}<br>` +
            `最低工资：${item.min}`
          this.salaryStatisticsData.push({
            name: item.name,
            value: item.value,
            tooltipText: tooltipText
          })
        })
      })
    },
    getDataByStatisticsClick() {
      this.getStatisticsData()
      this.$modal.msgSuccess("查询中，请稍候。。。")
    },
    handleToQuery(item, type) {
      if (!item && !item.name) return
      if (type === 'salary') {
        this.processSalaryQuery(item, type)
      } else {
        this.builderQuery(item, type)
      }
      this.getDataByStatisticsClick();
    },
    builderQuery(item, type) {
      this.query[type] = item.name;
      this.resetLabelQuery(type, item.name)
    },
    processSalaryQuery(item, type) {
      // 价格传过来的是'8k以下'、'10w-20w'等格式，解析成最小值和最大值
      const priceRange = this.parsePriceRange(item.name);
      this.query.maxSalary = priceRange.max;
      this.query.minSalary = priceRange.min;
      this.resetLabelQuery(type, item.name)
    },

    parsePriceRange(priceStr) {
      // 处理各种价格范围格式
      let minPrice = null;
      let maxPrice = null;
      console.log(priceStr)
      if (priceStr.includes('以下')) {
        // 如 '8k以下', '10w以下'
        const valueStr = priceStr.replace('以下', '');
        maxPrice = this.convertPrice(valueStr);
      } else if (priceStr.includes('以上')) {
        // 如 '200w以上', '10k以上'
        const valueStr = priceStr.replace('以上', '');
        minPrice = this.convertPrice(valueStr);
      } else if (priceStr.includes('-')) {
        // 如 '10w-20w', '8k-10k'
        const range = priceStr.split('-');
        minPrice = this.convertPrice(range[0]);
        maxPrice = this.convertPrice(range[1]);
      }

      return {min: minPrice, max: maxPrice};
    },

    convertPrice(priceStr) {
      // 将带单位的价格转换为数值，如 '8k' -> 8000, '10w' -> 100000
      priceStr = priceStr.toLowerCase();

      if (priceStr.includes('k')) {
        return parseFloat(priceStr.replace('k', '')) * 1000;
      } else if (priceStr.includes('w')) {
        return parseFloat(priceStr.replace('w', '')) * 10000;
      } else {
        return parseFloat(priceStr) || 0;
      }
    },
    // 重置标签查询
    resetLabelQuery(key, value) {
      this.tableQueryList.forEach(
        (table) => {
          if (table.key === key) {
            table.value = value;
          }
        }
      )
    },
    //点击速度排行榜
    clickTable(item) {
      if (item && item.seriesId) {
        const routeData = this.$router.resolve({
          name: 'SeriesDetail',
          params: {seriesId: item.seriesId}
        });
        window.open(routeData.href, '_blank');
      }
    },
    //重置查询
    reset() {
      this.query = {}
      let addressName = '全国'; // 默认值
      for (const item of this.tableQueryList) {
        if (item.key === 'address') {
          addressName = item.value;
          break;
        }
      }
      this.tableQueryList = baseQuery
      this.getDataByStatisticsClick();
      this.getMapData({
        name: addressName
      })
    }
  }
}
</script>
<style scoped lang="scss">
.app-container {
  background-image: url("../../../assets/images/map.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  padding: 0;
}

.map-chart-wrapper {
  height: 60vh;
}

.expert-chart-wrapper {
  height: 35vh;
}

.query-chart-wrapper {
  margin-top: 2vh;
  height: 25vh;
  margin-bottom: 2vh;
}

.center-chart-wrapper {
  height: 45vh;
}

.chart-wrapper {
  height: 35vh;
}

.rank-chart-wrapper {
  height: 42vh;
}

// 封面图片样式
.cover-image {
  width: 50px;
  height: 35px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background-color: rgba(255, 255, 255, 0.05);
  position: relative;
  // 加载中状态
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 16px;
    height: 16px;
    margin: -8px 0 0 -8px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top-color: #00d2ff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  &.lazy-loaded {
    background-color: transparent;

    &::before {
      display: none;
    }
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-image {
  color: #999;
  font-size: 12px;
}
</style>
