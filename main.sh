#!/bin/bash

# run_tests.sh - 运行测试并生成Allure报告

# 设置环境变量
export TEST_ENV="prod"
export TEST_IDC="shanghai"

echo "已设置环境变量:"
echo "TEST_ENV=$TEST_ENV"
echo "TEST_IDC=$TEST_IDC"

# 清理日志
rm -rf ./logs

# 清理之前的测试结果
rm -rf ./allure-results
rm -rf ./allure-report

# 清理之前的测试结果
rm -rf ./allure-results
rm -rf ./allure-report

# 创建结果目录
mkdir -p ./allure-results

# 运行pytest测试
echo "开始运行测试..."
pytest \
    -v \
    --alluredir=./allure-results \
    --clean-alluredir \
    --override-ini "allure_report_polish=false" \
    test_case/

# 检查pytest退出状态
if [ $? -ne 0 ]; then
    echo "警告: 部分测试失败!"
fi

# 生成Allure报告
echo "生成Allure报告..."
allure generate ./allure-results -o ./allure-report --clean

# 打开报告（可选）
echo "测试完成！报告位于: $(pwd)/allure-report/index.html"
# 取消下面一行的注释以自动打开报告
# xdg-open ./allure-report/index.html  # Linux
# open ./allure-report/index.html      # macOS
start ./allure-report/index.html     # Windows (Git Bash)