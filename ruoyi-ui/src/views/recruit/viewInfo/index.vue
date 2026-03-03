<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="编号" prop="id">
        <el-input
          v-model="queryParams.id"
          placeholder="请输入编号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="用户名" prop="userName">
        <el-input
          v-model="queryParams.userName"
          placeholder="请输入用户名"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
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
        <el-input
          v-model="queryParams.financingSituation"
          placeholder="请输入融资情况"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="分数" prop="score">
        <el-input
          v-model="queryParams.score"
          placeholder="请输入分数"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="创建时间" prop="createTime">
        <el-date-picker
          v-model="dateRangeCreateTime"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['recruit:viewInfo:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['recruit:viewInfo:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['recruit:viewInfo:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['recruit:viewInfo:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['recruit:viewInfo:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="viewInfoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="编号" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="id" />
      <el-table-column label="用户" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="userId" />
      <el-table-column label="用户名" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="userName" />
      <el-table-column label="岗位大类" align="center" v-if="columns[3].visible" prop="postType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_post_type" :value="scope.row.postType"/>
        </template>
      </el-table-column>
      <el-table-column label="城市等级" align="center" v-if="columns[4].visible" prop="cityLevel">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_city_level" :value="scope.row.cityLevel"/>
        </template>
      </el-table-column>
      <el-table-column label="省份" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible" prop="province" />
      <el-table-column label="城市" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible" prop="city" />
      <el-table-column label="薪资平均值" align="center" :show-overflow-tooltip="true" v-if="columns[7].visible" prop="salaryMonthAvg" />
      <el-table-column label="经验要求" align="center" v-if="columns[8].visible" prop="experienceRequired">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_experience_required" :value="scope.row.experienceRequired"/>
        </template>
      </el-table-column>
      <el-table-column label="学历要求" align="center" v-if="columns[9].visible" prop="educationRequired">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_education_required" :value="scope.row.educationRequired"/>
        </template>
      </el-table-column>
      <el-table-column label="主营业务" align="center" :show-overflow-tooltip="true" v-if="columns[10].visible" prop="mainBusiness" />
      <el-table-column label="企业规模" align="center" v-if="columns[11].visible" prop="enterpriseSize">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_enterprise_size" :value="scope.row.enterpriseSize"/>
        </template>
      </el-table-column>
      <el-table-column label="融资情况" align="center" v-if="columns[12].visible" prop="financingSituation">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.recruit_financing_situation" :value="scope.row.financingSituation"/>
        </template>
      </el-table-column>
      <el-table-column label="分数" align="center" :show-overflow-tooltip="true" v-if="columns[13].visible" prop="score" />
      <el-table-column label="创建时间" align="center" v-if="columns[14].visible" prop="createTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['recruit:viewInfo:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['recruit:viewInfo:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改用户浏览对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户" prop="userId">
          <el-input v-model="form.userId" placeholder="请输入用户" />
        </el-form-item>
        <el-form-item label="用户名" prop="userName">
          <el-input v-model="form.userName" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="岗位大类" prop="postType">
          <el-select v-model="form.postType" placeholder="请选择岗位大类">
            <el-option
              v-for="dict in dict.type.recruit_post_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="城市等级" prop="cityLevel">
          <el-select v-model="form.cityLevel" placeholder="请选择城市等级">
            <el-option
              v-for="dict in dict.type.recruit_city_level"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="form.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="form.city" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="薪资平均值" prop="salaryMonthAvg">
          <el-input v-model="form.salaryMonthAvg" placeholder="请输入薪资平均值" />
        </el-form-item>
        <el-form-item label="经验要求" prop="experienceRequired">
          <el-select v-model="form.experienceRequired" placeholder="请选择经验要求">
            <el-option
              v-for="dict in dict.type.recruit_experience_required"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学历要求" prop="educationRequired">
          <el-select v-model="form.educationRequired" placeholder="请选择学历要求">
            <el-option
              v-for="dict in dict.type.recruit_education_required"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="主营业务" prop="mainBusiness">
          <el-input v-model="form.mainBusiness" placeholder="请输入主营业务" />
        </el-form-item>
        <el-form-item label="企业规模" prop="enterpriseSize">
          <el-select v-model="form.enterpriseSize" placeholder="请选择企业规模">
            <el-option
              v-for="dict in dict.type.recruit_enterprise_size"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="融资情况" prop="financingSituation">
          <el-input v-model="form.financingSituation" placeholder="请输入融资情况" />
        </el-form-item>
        <el-form-item label="分数" prop="score">
          <el-input v-model="form.score" placeholder="请输入分数" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <div class="el-upload__tip" slot="tip">
            <el-checkbox v-model="upload.updateSupport" /> 是否更新已经存在的用户浏览数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;" @click="importTemplate">下载模板</el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>


import { listViewInfo, getViewInfo, delViewInfo, addViewInfo, updateViewInfo } from "@/api/recruit/viewInfo";
import { getToken } from "@/utils/auth";

export default {
  name: "ViewInfo",
  dicts: ['recruit_post_type', 'recruit_city_level', 'recruit_experience_required', 'recruit_education_required', 'recruit_enterprise_size', 'recruit_financing_situation'],
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 用户浏览表格数据
      viewInfoList: [],
      // 表格列信息
      columns: [
        { key: 0, label: '编号', visible: true },
        { key: 1, label: '用户', visible: true },
        { key: 2, label: '用户名', visible: true },
        { key: 3, label: '岗位大类', visible: true },
        { key: 4, label: '城市等级', visible: true },
        { key: 5, label: '省份', visible: true },
        { key: 6, label: '城市', visible: true },
        { key: 7, label: '薪资平均值', visible: true },
        { key: 8, label: '经验要求', visible: true },
        { key: 9, label: '学历要求', visible: true },
        { key: 10, label: '主营业务', visible: true },
        { key: 11, label: '企业规模', visible: true },
        { key: 12, label: '融资情况', visible: true },
        { key: 13, label: '分数', visible: true },
        { key: 14, label: '创建时间', visible: true }
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 创建时间时间范围
      dateRangeCreateTime: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        id: null,
        userName: null,
        postType: null,
        cityLevel: null,
        province: null,
        city: null,
        experienceRequired: null,
        educationRequired: null,
        mainBusiness: null,
        enterpriseSize: null,
        financingSituation: null,
        score: null,
        createTime: null
      },
      // 表单参数
      form: {},
      // 导入参数
      upload: {
        // 是否显示弹出层（导入）
        open: false,
        // 弹出层标题（导入）
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的用户浏览数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/recruit/viewInfo/importData"
      },
      // 表单校验
      rules: {
        id: [
          { required: true, message: "编号不能为空", trigger: "blur" }
        ],
        userId: [
          { required: true, message: "用户不能为空", trigger: "blur" }
        ],
        userName: [
          { required: true, message: "用户名不能为空", trigger: "blur" }
        ],
        score: [
          { required: true, message: "分数不能为空", trigger: "blur" }
        ],
        createTime: [
          { required: true, message: "创建时间不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询用户浏览列表 */
    getList() {
      this.loading = true;
      this.queryParams.params = {};
      if (null != this.dateRangeCreateTime && '' != this.dateRangeCreateTime.toString()) {
        this.queryParams.params["begincreateTime"] = this.dateRangeCreateTime[0];
        this.queryParams.params["endcreateTime"] = this.dateRangeCreateTime[1];
      }
      listViewInfo(this.queryParams).then(response => {
        this.viewInfoList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        id: null,
        userId: null,
        userName: null,
        postType: null,
        cityLevel: null,
        province: null,
        city: null,
        salaryMonthAvg: null,
        experienceRequired: null,
        educationRequired: null,
        mainBusiness: null,
        enterpriseSize: null,
        financingSituation: null,
        score: null,
        createTime: null
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRangeCreateTime = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加用户浏览";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getViewInfo(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改用户浏览";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.id != null) {
            updateViewInfo(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addViewInfo(submitData).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const viewInfoIds = row.id || this.ids;
      this.$modal.confirm('是否确认删除用户浏览编号为"' + viewInfoIds + '"的数据项？').then(function() {
        return delViewInfo(viewInfoIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('recruit/viewInfo/export', {
        ...this.queryParams
      }, `viewInfo_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "用户浏览导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "recruit/viewInfo/importTemplate",
        {},
        "viewInfo_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", { dangerouslyUseHTMLString: true });
      this.$modal.closeLoading()
      this.getList();
    },
    buildSubmitData() {
      const data = { ...this.form };
      if (data.id !== null && data.id !== undefined && data.id !== "") {
        data.id = parseInt(data.id, 10);
      } else {
        data.id = null;
      }
      if (data.userId !== null && data.userId !== undefined && data.userId !== "") {
        data.userId = parseInt(data.userId, 10);
      } else {
        data.userId = null;
      }
      if (data.salaryMonthAvg !== null && data.salaryMonthAvg !== undefined && data.salaryMonthAvg !== "") {
        data.salaryMonthAvg = parseFloat(data.salaryMonthAvg);
      } else {
        data.salaryMonthAvg = null;
      }
      if (data.score !== null && data.score !== undefined && data.score !== "") {
        data.score = parseFloat(data.score);
      } else {
        data.score = null;
      }
      return data;
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    }
  }
};
</script>
