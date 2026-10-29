<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import {
    NButton,
    NInput,
    NCard,
    NTag,
    NAlert,
    NSpace
} from 'naive-ui'

// State cho Form nhập
const rawArray = ref('3, 5, 8, 10, 12, 19, 22, 45, 60')
const targetValue = ref('19')

// State giao diện & kết quả
const loading = ref(false)
const errorMsg = ref('')
const resultData = ref<any>(null)
const currentStepIndex = ref(0)

// Chuyển chuỗi nhập thành mảng số
const parsedArray = computed(() => {
    return rawArray.value
        .split(',')
        .map((item) => parseInt(item.trim()))
        .filter((num) => !isNaN(num))
        .sort((a, b) => a - b)
})

// Gọi API FastAPI
const handleSimulate = async () => {
    loading.value = true
    errorMsg.value = ''
    resultData.value = null
    currentStepIndex.value = 0

    try {
        const target = parseInt(targetValue.value)
        if (isNaN(target)) {
            errorMsg.value = 'Vui lòng nhập một số hợp lệ cho giá trị target!'
            loading.value = false
            return
        }

        const response = await axios.post('http://127.0.0.1:8000/api/simulate/binary-search', {
            arr: parsedArray.value,
            target
        })

        resultData.value = response.data
    } catch (err: any) {
        errorMsg.value = 'Không thể kết nối đến server FastAPI. Bạn đã chạy backend ở cổng 8000 chưa?'
        console.error(err)
    } finally {
        loading.value = false
    }
}

// Lấy thông tin bước hiện tại để highlight
const currentStep = computed(() => {
    if (!resultData.value || !resultData.value.steps.length) return null
    return resultData.value.steps[currentStepIndex.value]
})

// Chức năng chuyển bước (Next / Prev)
const nextStep = () => {
    if (resultData.value && currentStepIndex.value < resultData.value.steps.length - 1) {
        currentStepIndex.value++
    }
}

const prevStep = () => {
    if (currentStepIndex.value > 0) {
        currentStepIndex.value--
    }
}
</script>

<template>
    <div class="min-h-screen bg-slate-900 text-slate-100 p-4 md:p-8 flex flex-col items-center">
        <header class="max-w-4xl w-full text-center mb-8">
            <h1
                class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500 mb-2">
                ⚡ Algorithm Visualizer
            </h1>
            <p class="text-slate-400">
                Mô phỏng thuật toán Tìm kiếm nhị phân (Binary Search) tương tác trực quan với FastAPI & Vue 3
            </p>
        </header>

        <main class="max-w-4xl w-full space-y-6">
            <!-- Card Cấu Hình Đầu Vào -->
            <NCard title="⚙️ Cấu hình dữ liệu đầu vào" class="bg-slate-800/80 border-slate-700 shadow-xl rounded-xl">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-300 mb-1">
                            Mảng số đầu vào (cách nhau bằng dấu phẩy):
                        </label>
                        <NInput v-model:value="rawArray" placeholder="3, 5, 8, 10, 12, 19, 22" size="large" />
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-end">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Giá trị cần tìm (Target):
                            </label>
                            <NInput v-model:value="targetValue" placeholder="Ví dụ: 19" size="large" />
                        </div>
                        <NButton type="primary" size="large" block :loading="loading" @click="handleSimulate"
                            class="font-semibold">
                            🚀 Chạy Mô Phỏng
                        </NButton>
                    </div>
                </div>
            </NCard>

            <!-- Alert Lỗi -->
            <NAlert v-if="errorMsg" type="error" class="rounded-xl">
                {{ errorMsg }}
            </NAlert>

            <!-- Kết Quả Mô Phỏng -->
            <div v-if="resultData" class="space-y-6">
                <!-- Visualization mảng số -->
                <NCard title="📊 Trực quan hóa thuật toán"
                    class="bg-slate-800/80 border-slate-700 shadow-xl rounded-xl">
                    <!-- Các chỉ số điều khiển bước -->
                    <div
                        class="flex items-center justify-between mb-6 bg-slate-900/60 p-3 rounded-lg border border-slate-700">
                        <span class="text-sm text-slate-300">
                            Bước: <strong class="text-teal-400">{{ currentStepIndex + 1 }}</strong> / {{
                            resultData.total_steps }}
                        </span>
                        <NSpace>
                            <NButton size="small" :disabled="currentStepIndex === 0" @click="prevStep">
                                ⬅️ Bước trước
                            </NButton>
                            <NButton size="small" type="primary"
                                :disabled="currentStepIndex === resultData.steps.length - 1" @click="nextStep">
                                Bước tiếp ➡️
                            </NButton>
                        </NSpace>
                    </div>

                    <!-- Các phần tử dạng Box -->
                    <div class="flex flex-wrap gap-2 justify-center my-6">
                        <div v-for="(val, idx) in resultData.sorted_array" :key="idx"
                            class="relative flex flex-col items-center justify-center w-14 h-16 rounded-lg font-mono text-lg font-bold transition-all duration-300 border-2"
                            :class="{
                                'bg-emerald-500/20 border-emerald-400 text-emerald-300 scale-110 shadow-lg shadow-emerald-500/20': currentStep && currentStep.mid === idx && currentStep.mid_value === resultData.target,
                                'bg-amber-500/20 border-amber-400 text-amber-300 scale-105': currentStep && currentStep.mid === idx && currentStep.mid_value !== resultData.target,
                                'bg-blue-500/10 border-blue-500/40 text-blue-300': currentStep && idx >= currentStep.left && idx <= currentStep.right && currentStep.mid !== idx,
                                'bg-slate-800/40 border-slate-700 text-slate-500 opacity-40': currentStep && (idx < currentStep.left || idx > currentStep.right)
                            }">
                            <span>{{ val }}</span>
                            <span class="text-[10px] font-normal text-slate-400 absolute bottom-1">
                                idx: {{ idx }}
                            </span>

                            <!-- Badge con trỏ Left/Right/Mid -->
                            <div class="absolute -top-6 flex gap-1 text-[10px] font-sans">
                                <span v-if="currentStep && currentStep.left === idx"
                                    class="bg-blue-600 text-white px-1 rounded">L</span>
                                <span v-if="currentStep && currentStep.mid === idx"
                                    class="bg-amber-600 text-white px-1 rounded">M</span>
                                <span v-if="currentStep && currentStep.right === idx"
                                    class="bg-purple-600 text-white px-1 rounded">R</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tóm tắt thông tin bước -->
                    <div v-if="currentStep"
                        class="bg-slate-900/80 p-4 rounded-lg text-sm space-y-2 border border-slate-700/50">
                        <div class="flex justify-between">
                            <span class="text-slate-400">So sánh:</span>
                            <span class="font-semibold text-teal-300">
                                Giá trị mid ({{ currentStep.mid_value }}) {{ currentStep.comparison === 'equal' ? '==' :
                                    (currentStep.comparison === 'greater' ? '>' : '<') }} {{ resultData.target }} </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-slate-400">Phạm vi tìm kiếm:</span>
                            <span>Index [{{ currentStep.left }} ... {{ currentStep.right }}]</span>
                        </div>
                    </div>
                </NCard>

                <!-- Kết quả tổng quan -->
                <NCard title="📌 Trạng thái kết quả" class="bg-slate-800/80 border-slate-700 shadow-xl rounded-xl">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                        <div class="p-3 bg-slate-900/50 rounded-lg">
                            <div class="text-xs text-slate-400 mb-1">Trạng thái</div>
                            <NTag :type="resultData.found ? 'success' : 'error'" size="large">
                                {{ resultData.found ? 'Tìm thấy' : 'Không tìm thấy' }}
                            </NTag>
                        </div>
                        <div class="p-3 bg-slate-900/50 rounded-lg">
                            <div class="text-xs text-slate-400 mb-1">Vị trí (Index)</div>
                            <div class="text-xl font-bold text-teal-400">
                                {{ resultData.found ? resultData.index : 'N/A' }}
                            </div>
                        </div>
                        <div class="p-3 bg-slate-900/50 rounded-lg">
                            <div class="text-xs text-slate-400 mb-1">Tổng số bước</div>
                            <div class="text-xl font-bold text-blue-400">
                                {{ resultData.total_steps }}
                            </div>
                        </div>
                    </div>
                </NCard>
            </div>
        </main>
    </div>
</template>

<style>
/* Tùy chỉnh theme dark cho Naive UI nếu muốn */
body {
    background-color: #0f172a;
}
</style>