import Alpine from 'alpinejs'

document.addEventListener('alpine:init', () => {

    Alpine.store('tasksView', {
        displayedTasks: [],
        currentView: 'inline',
        init() {
            console.log('tasks view store init ');
        },
        async updateViewWithTask(taskId) {
            const updatedTasks = await Alpine.store('tasksData').loadTasks();
            const updatedTask = updatedTasks.find(task => task.id === taskId)
            this.displayedTasks = this.displayedTasks.map(task => task.id === taskId ? updatedTask : task)
        },
        findById(taskId) {
            return this.displayedTasks.find(task => task.id === taskId)
        },
        switchView() {
            this.currentView === 'inline' ? this.currentView = 'kanban' : this.currentView = 'inline'
        },
    })

    Alpine.store('taskModal', {
        currentTask: null,

        previewModalHandle: null,
        deleteModalHandle: null,
        feedbackModalHandle: null,

        onPreviewClick(task) {
            this.currentTask = task
            console.log('preview click ? ', this.currentTask);
            this.previewModalHandle.show();
        },
        onDeleteClick(task) {
            this.currentTask = task
            this.deleteModalHandle.show();
        },
        onFeedbackClick(task) {
            this.currentTask = task
            this.feedbackModalHandle.show();
        }
    })
})

export default Alpine.store('tasksView')
