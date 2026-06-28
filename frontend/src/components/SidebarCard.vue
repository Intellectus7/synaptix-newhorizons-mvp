<script setup>
const props = defineProps({
    userId: Number,
    isBot: Boolean,
    lastMsg: String,
    avatar: String,
    username: String
})
</script>

<template>
    <div class="container">
        <div class="card">
            <div class="left">
                <div class="avatar">
                    {{ avatar }}
                </div>

                <div class="info">
                    <div class="top-row">
                        <span class="username">
                            {{ username }}
                        </span>

                        <span
                            class="bot-badge"
                            v-if="isBot"
                        >
                            AI
                        </span>
                    </div>

                    <p class="last-msg">
                        {{ lastMsg }}
                    </p>
                </div>
            </div>

            <div class="chevron">
                →
            </div>
        </div>
    </div>
</template>

<style scoped>

.container{
    width:100%;
}

.card{
    background: rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;

    padding:1rem 1.2rem;

    display:flex;
    justify-content:space-between;
    align-items:center;

    cursor:pointer;

    transition:
        transform .18s ease,
        background .18s ease,
        border-color .18s ease;
}

.card:hover{
    transform:translateY(-2px);

    background:rgba(255,255,255,.07);

    border-color:rgba(255,255,255,.15);
}

.left{
    display:flex;
    align-items:center;
    gap:1rem;

    min-width:0;
}

.avatar{
    width:56px;
    height:56px;

    border-radius:50%;

    display:flex;
    justify-content:center;
    align-items:center;

    font-size:1.8rem;

    background:rgba(255,255,255,.06);

    flex-shrink:0;
}

.info{
    min-width:0;
}

.top-row{
    display:flex;
    align-items:center;
    gap:.5rem;

    margin-bottom:.25rem;
}

.username{
    font-weight:700;
    font-size:1.05rem;
}

.bot-badge{
    font-size:.65rem;

    background:#6b5cff;

    padding:.18rem .45rem;

    border-radius:999px;

    font-weight:700;
}

.last-msg{
    color:#b8b8b8;

    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;

    margin:0;
}

.chevron{
    font-size:1.3rem;

    color:#888;

    transition:transform .2s;
}

.card:hover .chevron{
    transform:translateX(4px);
}

</style>
