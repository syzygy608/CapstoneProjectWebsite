<script setup>
import { ref } from 'vue'
import axios from 'axios'

const showTest = ref(false);
const problemIndex = ref(1);
const showResult = ref(false);

const table = [ [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ];

const type = ref(["偶像服裝", "地雷系服裝", "日常服", "泳裝"]);

const input = ref("");

const startTest = () => {
    showTest.value = true;
}

const nextProblem = () => {
    if(problemIndex.value < 4)
    {
        input.value = input.value.trim();
        // use regular expression to check if the input is valid
        if(input.value == "")
        {
            alert("請輸入你的喜好順序");
            return;
        }
        if(!/^\d{1} \d{1} \d{1} \d{1}$/.test(input.value))
        {
            alert("請輸入四個數字，以空白隔開，並且數字範圍為1~4");
            input.value = "";
            return;
        }
        const order = input.value.split(" ");
        if((1 ^ 2 ^ 3 ^ 4 ^ order[0] ^ order[1] ^ order[2] ^ order[3]) != 0)
        {
            alert("請輸入1~4的數字");
            input.value = "";
            return;
        }
        for(let i = 0; i < 4; i++)
            for(let j = i + 1; j < 4; j++)
                table[order[i] - 1][order[j] - 1] += 1;
        problemIndex.value += 1;
        input.value = "";
    }
    else
    {
        console.log(table);
        axios.post("http://127.0.0.1:5000/predict", table)
            .then((response) => {
                console.log(response.data);
                let tmp = [];
                for(let i = 0; i < 4; i++)
                    tmp.push([type.value[i], response.data[i]]);
                // Sort the array by the second element
                tmp.sort((a, b) => b[1] - a[1]);
                for(let i = 0; i < 4; i++)
                    type.value[i] = tmp[i][0];
                showResult.value = true;

            })
            .catch((error) => {
                console.log(error);
            });
    }
}
</script>

<template>
    <div class = "min-h-[calc(100vh-3rem)] flex justify-center items-center bg-purple-100 flex-col">
        <div v-show="!showTest && !showResult" class = "justify-center flex items-center flex-col">
            <div class = "text-2xl text-gray-600">
                在本測驗中，每題會有四張照片，請依照你的喜歡程度排出順序，最後會根據你的回答給出結果。
            </div>
            <div>
                <button class = "bg-purple-300 text-white px-4 py-2 rounded-lg mt-4 hover:bg-purple-600" v-on:click="startTest">
                    開始測驗
                </button>
            </div>
        </div>
        <div v-show = "showTest && !showResult" class = "justify-center flex items-center flex-col">
            <div class="grid grid-cols-2 gap-4 w-[50rem] relative">
                <div class="relative">
                    <img :src="`/Idol/0${problemIndex}.png`" alt="Idol" class="w-full p-2">
                    <div class="absolute bottom-2 right-2 bg-white/50 text-black w-6 h-6 flex items-center justify-center">1</div>
                </div>
                <div class="relative">
                    <img :src="`/Jiraikei/0${problemIndex}.png`" alt="Jiraikei" class="w-full p-2">
                    <div class="absolute bottom-2 right-2 bg-white/50 text-black w-6 h-6 flex items-center justify-center">2</div>
                </div>
                <div class="relative">
                    <img :src="`/Normal/0${problemIndex}.png`" alt="Normal" class="w-full p-2">
                    <div class="absolute bottom-2 right-2 bg-white/50 text-black w-6 h-6 flex items-center justify-center">3</div>
                </div>
                <div class="relative">
                    <img :src="`/Swimsuit/0${problemIndex}.png`" alt="Swimsuit" class="w-full p-2">
                    <div class="absolute bottom-2 right-2 bg-white/50 text-black w-6 h-6 flex items-center justify-center">4</div>
                </div>
            </div>
            <input type = "text" class = "w-1/2 mt-4 p-2 border-2 border-purple-300 rounded-lg" placeholder="請輸入你的喜好順序，以空白隔開，例如 3 4 1 2" v-model="input">
            <button class = "bg-purple-300 text-white px-4 py-2 rounded-lg mt-4 hover:bg-purple-600" v-on:click="nextProblem">
                下一題
            </button>
        </div>
        <div v-show="showResult" class = "justify-center flex items-center flex-col">
            <div class = "text-2xl text-gray-600">
                你的衣裝風格偏好為：
            </div>
            <div class = "text-2xl text-gray-600">
                {{ type[0] }} > {{ type[1] }} > {{ type[2] }} > {{ type[3] }}
            </div>
        </div>
    </div>
</template>