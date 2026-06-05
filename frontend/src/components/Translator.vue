<template>
  <div class="page">

```
<div class="translator-card">

  <h1>🌍 智能翻译机</h1>

  <textarea
    v-model="text"
    placeholder="请输入中文、英文、单词或句子..."
  ></textarea>

  <button @click="translate">
    翻译
  </button>

  <div
    class="result-card"
    v-if="result"
  >

    <h2>翻译结果</h2>

    <p class="translation">
      {{ result }}
    </p>

    <div
      v-if="wordInfo"
      class="word-info"
    >

      <div class="tag">
        音标：{{ wordInfo.phonetic || "暂无" }}
      </div>

      <div class="tag">
        词性：{{ wordInfo.pos || "暂无" }}
      </div>

    </div>

  </div>

  <div
    class="example-card"
    v-if="wordInfo && wordInfo.example"
  >

    <h2>📖 例句</h2>

    <div class="example-box">

      <p class="english">
        {{ wordInfo.example }}
      </p>

      <p class="chinese">
        {{ wordInfo.example_zh }}
      </p>

    </div>

  </div>

  <div class="history-card">

    <div class="history-header">

      <h2>🕒 历史记录</h2>

      <button
        class="clear-btn"
        @click="clearHistory"
      >
        清空
      </button>

    </div>

    <div class="history-list">

      <div
        class="history-item"
        v-for="item in history"
        :key="item.id"
      >

        <p>
          <strong>原文：</strong>
          {{ item.source }}
        </p>

        <p>
          <strong>译文：</strong>
          {{ item.result }}
        </p>

        <small>
          {{ item.time }}
        </small>

      </div>

    </div>

  </div>

</div>
```

  </div>
</template>

<script setup>
import axios from "axios"
import { ref,onMounted } from "vue"

const API="http://127.0.0.1:5000"

const text=ref("")
const result=ref("")
const history=ref([])
const wordInfo=ref(null)

const translate=async()=>{

  if(!text.value.trim()) return

  try{

    const res=await axios.post(
      `${API}/translate`,
      {
        text:text.value
      }
    )

    result.value=res.data.result

    wordInfo.value=res.data.word_info

    loadHistory()

  }catch(error){

    console.error(error)

    result.value="翻译失败"

    wordInfo.value=null
  }
}

const loadHistory=async()=>{

  try{

    const res=await axios.get(
      `${API}/history`
    )

    history.value=res.data

  }catch(error){

    console.error(error)
  }
}

const clearHistory=async()=>{

  try{

    await axios.delete(
      `${API}/clear`
    )

    history.value=[]

  }catch(error){

    console.error(error)
  }
}

onMounted(()=>{
  loadHistory()
})
</script>

<style>
*{
  margin:0;
  padding:0;
  box-sizing:border-box;
}

body{
  font-family:"Microsoft YaHei";
}

.page{
  min-height:100vh;
  background:linear-gradient(
    135deg,
    #4facfe,
    #00f2fe
  );
  display:flex;
  justify-content:center;
  align-items:center;
  padding:30px;
}

.translator-card{
  width:900px;
  background:white;
  border-radius:20px;
  padding:30px;
  box-shadow:0 10px 30px rgba(0,0,0,.15);
}

h1{
  text-align:center;
  margin-bottom:20px;
}

textarea{
  width:100%;
  height:150px;
  padding:15px;
  font-size:18px;
  border:2px solid #ddd;
  border-radius:12px;
  resize:none;
  outline:none;
}

textarea:focus{
  border-color:#4facfe;
}

button{
  margin-top:15px;
  padding:12px 30px;
  border:none;
  border-radius:10px;
  background:#4facfe;
  color:white;
  font-size:16px;
  cursor:pointer;
  transition:.3s;
}

button:hover{
  transform:translateY(-2px);
}

.result-card,
.example-card,
.history-card{
  margin-top:25px;
  background:#f8f9fa;
  padding:20px;
  border-radius:15px;
}

.translation{
  margin-top:15px;
  font-size:24px;
  color:#333;
  font-weight:bold;
}

.word-info{
  display:flex;
  gap:15px;
  margin-top:15px;
}

.tag{
  background:#4facfe;
  color:white;
  padding:8px 15px;
  border-radius:20px;
}

.example-box{
  margin-top:15px;
}

.english{
  font-size:18px;
  color:#222;
}

.chinese{
  margin-top:10px;
  color:#666;
}

.history-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.clear-btn{
  background:#ff4d4f;
}

.history-list{
  margin-top:15px;
  max-height:300px;
  overflow-y:auto;
}

.history-item{
  background:white;
  padding:15px;
  margin-bottom:10px;
  border-radius:10px;
  border-left:5px solid #4facfe;
}

.history-item small{
  color:#888;
}
</style>
