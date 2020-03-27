<template>
    <div class="page-header">
        <v-img src="../assets/app-bar.png" height="150"></v-img>
        <div class="page-header-content">
            <div class="d-flex justify-space-between">
                <div class="logo-section">
                    <img src="../assets/logo.png" height="20">
                    <img class="ml-1" src="../assets/crm.png" height="15">
                </div>
                <div class="menu caption pa-7">
                    <a to="/forest">森林情報一覧</a>
                    <a class="ml-4 mr-4" to="forest">顧客情報一覧</a>
                    <a class="mr-4" to="forest">交渉履歴一覧</a>
                    <a to="forest">設定</a>
                </div>
            </div>
            <div>
                <v-icon class="icon-mode">mdi-image-filter-hdr</v-icon>
                <span class="ml-4 white--text">森林管理</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'page-header'
}
</script>

<style lang="scss">
.page-header {
    position: relative;

    .page-header-content {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background: linear-gradient(87.07deg, #1B756A 0%, rgba(196, 196, 196, 0) 100%);

        .logo-section {
            padding: 28px;
        }

        .menu {
            a {
                color: white;
            }
        }

        .icon-mode {
            background-color: white;
            margin-left: 28px;
            height: 40px;
            width: 40px;
            padding: 15px;
            border-radius: 50%;
        }
    }
}
</style>
