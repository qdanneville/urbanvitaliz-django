import Alpine from 'alpinejs'
import TaskApp from './Tasks'
import { TASK_STATUSES } from '../config/statuses';
import { NO_TOPICS } from '../config/tasks';

export default function TasksInline(projectId) {

    const app = {
        filterIsDraft: false,
        boardsFiltered: [],
        boards: [
            { status: [TASK_STATUSES.PROPOSED,TASK_STATUSES.INPROGRESS,TASK_STATUSES.BLOCKED,TASK_STATUSES.DONE,TASK_STATUSES.NOT_INTERESTED], title: "Nouvelles", color_class: "border-error", color: "#0d6efd" },
        ],
        init() {
            this.boardsFiltered = this.boards
        },
        async handleDraftFilterChange() {

            this.filterIsDraft = !this.filterIsDraft

            await this.getData();

            this.updateView()
        },
        async publishTask(taskId) {
            await this.$store.tasksData.patchTask(taskId, { public: true });
            await this.$store.tasksData.loadTasks();
            // this.updateView()
        },
        updateView() {
            if (!this.filterIsDraft) return

            return this.data = this.data.filter((d) => d.public == !this.filterIsDraft);
        },
        filterTaskByTopic(topic) {
            return this.view.filter(data => {
                if (data.topic) {
                    return data.topic.name === topic
                } else if (topic === NO_TOPICS) {
                    return true
                }
            })
        }
    }

    return TaskApp(app, projectId);
}

Alpine.data("TasksInline", TasksInline)
