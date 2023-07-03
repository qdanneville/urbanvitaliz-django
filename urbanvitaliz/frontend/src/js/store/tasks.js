import Alpine from 'alpinejs'
import api, { tasksUrl,taskUrl, moveTaskUrl, followupsUrl, taskNotificationsUrl, markTaskNotificationsAsReadUrl } from '../utils/api'
import { generateUUID } from '../utils/uuid'

Alpine.store('tasksView', {
    currentView: 'inline',
    init() {
        console.log('tasks view store init ');
    },
    switchView() {
        this.currentView === 'inline' ? this.currentView = 'kanban' : this.currentView = 'inline'
    },
})

Alpine.store('tasksData', {
    projectId: null,
    tasks: [],
    canUseTasks:false,
    canManageTasks:false,
    init() {
        console.log('tasks data store init ');
    },
    async getTasks(projectId) {

        if (!this.projectId) {
            this.projectId = projectId
        }
        
        const json = await api.get(tasksUrl(this.projectId))

        const data = json.data.map(d => Object.assign(d, {
            uuid: generateUUID()
        }));

        return this.tasks = data;
    },
    async moveTask(taskId, otherTaskId, below) {
        const params = new URLSearchParams(`${below ? 'below' : 'above'}=${otherTaskId}`);
        await api.post(moveTaskUrl(this.projectId, taskId), params, {
            headers: { 'content-type': 'application/x-www-form-urlencoded' },
        })
    },
    // Movement Buttons
    async moveAbove(task, otherTask) {
        await this.moveTask(task.id, otherTask.id);
        await this.getTasks();
    },
    async moveBelow(task, otherTask) {
        await this.moveTask(task.id, otherTask.id, true);
        await this.getTasks();
    },
    async patchTask(taskId, patch) {
        await api.patch(taskUrl(this.projectId, taskId), patch)
    },
})

Alpine.store('task', {
    projectId: null,
    init() {
        console.log('current task store init ');
    },
    initProject(projectId) {
        this.projectId = projectId
        console.log('project task sotre ? ', this.projectId)
    },
    async loadFollowups(taskId) {
        const { data } = await api.get(followupsUrl(this.projectId, taskId));
        console.log('data qsdjklqsdjkljklqsdljk ', data);
        return data
    },
    async loadNotifications(taskId) {
        const { data } = await api.get(taskNotificationsUrl(this.projectId, taskId));
        return data;
    },
    async issueFollowup(task, status, comment = "") {
        const body = { comment, status }

        if (body.status === task.status && body.comment === "") return;

        await api.post(followupsUrl(this.projectId, task.id), body)
    },
    async editComment(taskId, followupId, comment) {
        await api.patch(followupUrl(this.projectId, taskId, followupId), { comment })
    },
    async markAllAsRead(taskId) {
        await api.post(markTaskNotificationsAsReadUrl(this.projectId, taskId), {})
    },
})

Alpine.store('taskModal', {
    currentTask:null,
    previewModalHandle:null,
    deleteModalHandle:null,
    feedbackModalHandle:null,
    onPreviewClick(task) {
        this.currentTask = task
        console.log('preview click ? ', this.currentTask);
        this.previewModalHandle.show();
    },
    onDeleteClick(task) {
        this.currentTask = task
        console.log('delete task ', this.currentTask);
        this.deleteModalHandle.show();
    }
})

export default Alpine.store('tasks')
