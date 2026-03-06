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
          <PiePetalTransparentPoseCharts
            :chart-data="countrySalesStatisticsData"
            :chart-title="countrySalesStatisticsName"
            @item-click="(item) => handleToQuery(item, 'country')"
            :label-show-value="false"
          />
        </div>
        <div class="chart-wrapper">
          <div class="chart-wrapper">
            <TableRanking
              :columns="tableColumns"
              :data="accelerationStatisticsData"
              @rowClicked="clickTable"
            >
              <!-- 封面图片插槽 -->
              <template slot="coverImage" slot-scope="{ row }">
                <img
                  v-if="row.coverImage"
                  v-lazy
                  :data-src="row.coverImage"
                  :alt="row.name || '封面'"
                  class="cover-image"
                />
                <span v-else class="no-image">暂无图片</span>
              </template>
            </TableRanking>
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
          <BarLineZoomCharts
            :chart-title="salesPredictStatisticsName"
            :chart-data="salesPredictStatisticsData"
          />
        </div>
        <div class="center-chart-wrapper">
          <KeywordGravityCharts
            :font-size-range="[12,36]"
            :chart-data="brandSalesStatisticsData"
            :chart-name="brandSalesStatisticsName"
            @item-click="(item) => handleToQuery(item, 'brandName')"/>
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
          <BarRankingZoomCharts
            :chart-data="seriesSalesStatisticsData"
            :chart-title="seriesSalesStatisticsName"
            :displayCount="12"
            @item-click="(item) => handleToQuery(item, 'seriesName')"/>
        </div>
        <div class="chart-wrapper">
          <PieGradientRoseCharts
            :label-show-value="false"
            :chart-data="monthSalesStatisticsData"
            :chart-title="monthSalesStatisticsName"
            :max-label-length="6"
          />
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
import {cityLevelStatistics, educationStatistics, mapStatistics, postTypeStatistics} from "@/api/recruit/statistics";
import PieLayerRateCharts from "@/components/Echarts/PieLayerRateCharts.vue";

export default {
  name: "SalesStatisticsScreen",
  components: {
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
      tableQueryList: [
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
      ],
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
      //价格销量
      priceSalesStatisticsData: [],
      priceSalesStatisticsName: "价格销量分析",
      priceSalesStatisticsNameOrigin: "价格销量分析",
      //能源类型
      energyTypeSalesStatisticsData: [],
      energyTypeSalesStatisticsName: "能源类型分析",
      energyTypeSalesStatisticsNameOrigin: "能源类型分析",
      //品牌
      brandSalesStatisticsData: [],
      brandSalesStatisticsName: "品牌分析",
      brandSalesStatisticsOrigin: "品牌",
      //国家
      countrySalesStatisticsData: [],
      countrySalesStatisticsName: "国家分析",
      countrySalesStatisticsNameOrigin: "国家分析",
      //车型
      modelTypeSalesStatisticsData: [],
      modelTypeSalesStatisticsName: "车型分析",
      modelTypeSalesStatisticsNameOrigin: "车型分析",
      //月份
      monthSalesStatisticsData: [],
      monthSalesStatisticsName: "月份销量分析",
      monthSalesStatisticsNameOrigin: "月份销量分析",
      //车系
      seriesSalesStatisticsData: [],
      seriesSalesStatisticsName: "车系排行",
      seriesSalesStatisticsNameOrigin: "车系排行",
      //销量预测
      salesPredictStatisticsData: [],
      salesPredictStatisticsName: "销量预测",
      salesPredictStatisticsNameOrigin: "销量预测",
      //百公里加速
      accelerationStatisticsData: [],
      accelerationStatisticsName: "百公里加速",
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
      this.getStatisticsData()
    },
    getStatisticsData() {
      this.getMapStatisticsData()
      this.getCityLevelStatisticsData()
      this.getPostTypeStatisticsData()
      this.getEducationStatisticsData()
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
        address: this.query.address
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
        address: this.query.address
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
        address: this.query.address
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
    getDataByStatisticsClick() {
      this.getMapStatisticsData()
      this.$modal.msgSuccess("查询中，请稍候。。。")
    },
    handleToQuery(item, type) {
      if (!item && !item.name) return
      if (type === 'cityLevel') {
        this.processCityLevelQuery(item, type)
      }
      if (type === 'postType') {
        this.processPostTypeQuery(item, type)
      }
      if (type === 'education') {
        this.processEducationQuery(item, type)
      }
      if (type === 'price') {
        this.processPriceQuery(item, type)
      }
      this.getDataByStatisticsClick();
    },
    processEducationQuery(item, type) {
      this.query.education = item.name;
      this.resetLabelQuery(type, item.name)
    },
    processCityLevelQuery(item, type) {
      this.query.cityLevel = item.name;
      this.resetLabelQuery(type, item.name)
    },
    processPostTypeQuery(item, type) {
      this.query.postType = item.name;
      this.resetLabelQuery(type, item.name)
    },
    processPriceQuery(item, type) {
      // 价格传过来的是'8k以下'、'10w-20w'等格式，解析成最小值和最大值
      const priceRange = this.parsePriceRange(item.name);
      this.query.minPrice = priceRange.min;
      this.query.maxPrice = priceRange.max;
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
      this.query = {
        startTime: this.query.startTime,
        endTime: this.query.endTime,
        minPrice: null,
        maxPrice: null,
        modelType: null,
        brandName: null,
        country: null,
        energyType: null,
        seriesId: null
      }
      let addressName = '全国'; // 默认值
      for (const item of this.tableQueryList) {
        if (item.key === 'address') {
          addressName = item.value;
          break;
        }
      }
      this.tableQueryList = [
        {
          label: '品牌',
          value: '全部',
          key: 'brandName',
        },
        {
          label: '价格',
          value: '全部',
          key: 'price',
        },
        {
          label: '车型',
          value: '全部',
          key: 'modelType',
        },
        {
          label: '能源',
          value: '全部',
          key: 'energyType',
        },
        {
          label: '国家',
          value: '全部',
          key: 'country',
        },
        {
          label: '车系',
          value: '全部',
          key: 'seriesName',
        },
        {
          label: '地区',
          value: addressName,
          key: 'address',
        },
      ]
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
