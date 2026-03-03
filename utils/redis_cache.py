import asyncio
import os
import time
from pathlib import Path

import redis.asyncio as redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from utils.log_config import get_logger

logger = get_logger(__name__)


class AsyncMessageMemoryDAO:
    def __init__(self, mysql_cfg=None):
        """
        初始化异步连接池（MySQL + Redis）
        """
        self.redis = None
        self.redis_cfg = {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": REDIS_DB,
            "password": REDIS_PASSWORD
        }
        self.redis = None

    # ---------- 初始化 ----------
    async def init_pools(self):
        try:
            """初始化Redis 连接池"""
            if not self.redis:
                redis_url = f"redis://{self.redis_cfg['host']}:{self.redis_cfg['port']}/{self.redis_cfg['db']}"
                if self.redis_cfg['password']:
                    redis_url = f"redis://:{self.redis_cfg['password']}@{self.redis_cfg['host']}:{self.redis_cfg['port']}/{self.redis_cfg['db']}"

                self.redis = await redis.from_url(
                    redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                )
                try:
                    await self.redis.ping()
                except Exception as e:
                    logger.error(f"❌ Redis连接失败: {e}")
                    raise e
                logger.info("✅ Redis cache connection established")
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            raise e

    # 标记 message 已被撤回
    async def mark_deleted(self, message_id: str):
        await self.redis.set(f"deleted:{message_id}", "1", ex=60)  # 防止占空间，可设置过期

    # 查询 message 是否被撤回
    async def is_deleted(self, message_id: str) -> bool:
        return await self.redis.exists(f"deleted:{message_id}") == 1

    async def set_flag(self, key, value):
        """设置 Redis 中的标志位"""
        try:
            await self.redis.set(key, value, 180)
            logger.info(f"✅ 标志位 '{key}' 设置为: {value}")
        except Exception as e:
            logger.error(f"⚠️ 设置标志位时发生错误: {e}")

    async def close_redis(self):
        if self.redis:
            await self.redis.aclose()
            # await self.redis.wait_closed()
            logger.info("✅ Redis connection pool closed.")


# ✅ 在模块加载时就初始化连接池（异步安全）
async def init_dao():
    await dao.init_pools()


# ✅ 创建全局唯一 DAO 实例
dao = AsyncMessageMemoryDAO()


async def pure_redis_benchmark():
    # 2. 建立连接
    await init_dao()

    try:
        # 确保连接正常
        await dao.redis.ping()

        test_key = "perf_test_key"
        test_value = "Hello Redis Speed Test"
        loop_count = 10000

        print(f"🚀 开始纯净测试：循环 Set/Get 各 {loop_count} 次...\n")

        # --- 测试 SET 性能 ---
        start_set = time.perf_counter()
        for i in range(loop_count):
            await dao.redis.set(f"{test_key}:{i}", test_value)
        end_set = time.perf_counter()

        set_duration = end_set - start_set
        print(f"💾 [SET] 总耗时: {set_duration:.4f}s | QPS: {int(loop_count / set_duration)}")

        # --- 测试 GET 性能 ---
        start_get = time.perf_counter()
        for i in range(loop_count):
            await dao.redis.get(f"{test_key}:{i}")
        end_get = time.perf_counter()

        get_duration = end_get - start_get
        print(f"🔍 [GET] 总耗时: {get_duration:.4f}s | QPS: {int(loop_count / get_duration)}")

        # --- 统计单次延迟 ---
        avg_latency = (get_duration / loop_count) * 1000
        print(f"\n⏱️ 平均单次 Get 延迟: {avg_latency:.4f} ms")

        # --- 清理测试数据 ---
        # 批量删除测试 key (可选)
        # await client.flushdb()

    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        await dao.redis.close()


if __name__ == "__main__":
    asyncio.run(pure_redis_benchmark())
