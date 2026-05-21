
"""
向量检索模块
"""
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from product_database import PRODUCTS
from config import VECTOR_MODEL


class VectorSearchEngine:
    def __init__(self):
        self.model = None
        self.index = None
        self.product_descriptions = []
        self.product_ids = []
        
    def load_model(self):
        """加载向量模型"""
        if self.model is None:
            print("正在加载向量模型...")
            self.model = SentenceTransformer(VECTOR_MODEL)
            self._build_index()
            
    def _build_index(self):
        """构建FAISS索引"""
        self.product_descriptions = []
        self.product_ids = []
        
        for product in PRODUCTS:
            desc = f"{product['name']} {product['description']} 适合温度{product['min_temp']}-{product['max_temp']}℃ 场合:{','.join(product['occasions'])}"
            self.product_descriptions.append(desc)
            self.product_ids.append(product["id"])
            
        embeddings = self.model.encode(self.product_descriptions, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        print("向量索引构建完成")
        
    def search(self, query: str, top_k: int = 3) -&gt; List[Dict]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            匹配的商品列表
        """
        self.load_model()
        
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx in indices[0]:
            product_id = self.product_ids[idx]
            for product in PRODUCTS:
                if product["id"] == product_id:
                    results.append(product)
                    break
                    
        return results


def semantic_search(query: str, top_k: int = 3) -&gt; List[Dict]:
    """
    便捷函数：语义搜索
    
    Args:
        query: 查询文本
        top_k: 返回数量
        
    Returns:
        匹配的商品列表
    """
    engine = VectorSearchEngine()
    return engine.search(query, top_k)


if __name__ == "__main__":
    query = "我需要一件适合约会的优雅连衣裙，天气20度左右"
    results = semantic_search(query)
    print(f"搜索结果 ({len(results)}):")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product['name']}")
        print(f"   {product['description']}")
        print()
