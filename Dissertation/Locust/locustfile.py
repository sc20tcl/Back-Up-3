from locust import HttpUser, between, task

class TeaStoreUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_teastore(self):
        self.client.get("/")

    @task(3)  # higher weight means this task is executed 3 times more often
    def browse_products(self):
        self.client.get("/tools.descartes.teastore.webui/category?category=2&page=1")
        self.client.get("/tools.descartes.teastore.webui/product?id=12")
        self.client.get("/tools.descartes.teastore.webui/product?id=210")
        self.client.get("/tools.descartes.teastore.webui/cart")
        self.client.get("/tools.descartes.teastore.webui/login")

