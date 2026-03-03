<template>
  <div class="app-container">
    <!-- 欢迎标题 -->
    <div class="welcome-section">
      <h1 class="welcome-title">欢迎使用 {{ title }}，{{ username }}</h1>
      <p class="welcome-subtitle">根据您的浏览和点赞记录，为您推荐以下岗位</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <i class="el-icon-loading"></i>
      <span>加载推荐中...</span>
    </div>

    <!-- 统计信息 -->
    <div class="total-info" v-if="!loading && recommendList.length > 0">
      <span class="total-text">为您推荐了 <strong>{{ total }}</strong> 个岗位</span>
    </div>

    <!-- 卡片列表容器 -->
    <div
      class="card-container masonry-container"
      v-loading="loading"
    >
      <div class="masonry-wrapper">
        <div
          v-for="item in recommendList"
          :key="item.recruitId"
          class="masonry-item"
        >
          <!-- 使用招聘卡片组件 -->
          <recruit-card :item="item"/>
        </div>
      </div>

      <!-- 加载更多 -->
      <div class="load-more-tip" v-if="hasMore">
        <i class="el-icon-loading" v-if="loadingMore"></i>
        <span>{{ loadingMore ? '加载中...' : '滚动加载更多' }}</span>
      </div>
      <div class="load-more-tip no-more" v-if="!hasMore && recommendList.length > 0">
        <span>没有更多数据了</span>
      </div>

      <!-- 空状态 -->
      <div class="empty-tip" v-if="!loading && recommendList.length === 0">
        <el-empty description="暂无推荐，请先浏览或点赞一些岗位">
          <el-button type="primary" @click="$router.push({name:'RecruitInfoQuery'})">去浏览岗位</el-button>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<script>
import {getRecommendContent} from "@/api/recruit/recommendInfo";
import RecruitCard from "../components/index/RecruitCard.vue";

export default {
  name: 'Index',
  components: {
    RecruitCard
  },
  data() {
    return {
      title: process.env.VUE_APP_TITLE,
      // 用户名
      username: '',
      // 遮罩层
      loading: false,
      // 加载更多中
      loadingMore: false,
      // 推荐列表
      recommendList: [],
      // 总条数
      total: 0,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 20
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
    // 获取当前用户名
    this.username = this.$store.state.user.name || '用户';
    console.log(this.$store.state.user)
    console.log(this.username);
    // 加载推荐列表
    this.getRecommendList();
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
    /** 获取推荐列表（自动判断是否需要生成新推荐） */
    getRecommendList(reset = false) {
      if (reset) {
        this.queryParams.pageNum = 1;
        this.recommendList = [];
        this.hasMore = true;
        this.loading = true;
      } else {
        this.loadingMore = true;
      }

      getRecommendContent(this.queryParams).then(response => {
        if (reset) {
          this.recommendList = response.rows || [];
        } else {
          this.recommendList = [...this.recommendList, ...(response.rows || [])];
        }
        this.total = response.total || 0;

        // 判断是否还有更多数据
        this.hasMore = this.recommendList.length < this.total;

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
      this.getRecommendList(false);
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

.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #fff;

  .welcome-title {
    margin: 0 0 10px 0;
    font-size: 28px;
    font-weight: 600;
  }

  .welcome-subtitle {
    margin: 0;
    font-size: 16px;
    opacity: 0.9;
  }
}

.loading-container {
  text-align: center;
  padding: 60px 0;
  color: #909399;
  font-size: 14px;

  i {
    font-size: 24px;
    margin-right: 10px;
    display: block;
    margin-bottom: 10px;
  }
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

  .welcome-section {
    padding: 20px;

    .welcome-title {
      font-size: 22px;
    }

    .welcome-subtitle {
      font-size: 14px;
    }
  }
}
</style>
