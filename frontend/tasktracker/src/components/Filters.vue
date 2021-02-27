<template>
    <div>
        <b-button-toolbar>
            <b-button-group class="my-2 mx-2">
                <b-button variant="success">Day</b-button>
                <b-button variant="success">Week</b-button>
                <b-button variant="success">Month</b-button>
                <b-button variant="success">Year</b-button>
                <b-button variant="success">Global</b-button>
                <b-button variant="success">Free</b-button>
            </b-button-group>

            <b-button-group class="my-2 mx-2">
                <b-button variant="success">&lt;&lt; Prev</b-button>
                <b-button variant="success">Current</b-button>
                <b-button variant="success">Next &gt;&gt;</b-button>
            </b-button-group>

            <b-dropdown class="my-2 mx-2" right text="Filters">
                <b-dropdown-item>All</b-dropdown-item>
                <b-dropdown-item>Habits</b-dropdown-item>
            </b-dropdown>
        </b-button-toolbar>
    </div>
</template>

<script>
export default {
}
</script>

<style scoped>
b-button-toolbar {
    margin-top: 10px;
}
</style>