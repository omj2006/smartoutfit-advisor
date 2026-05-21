
"""
向量检索工具模块
"""
import numpy as np
from utils.db_tools import PRODUCTS

# 容错导入 sentence-transformers
sentence_transformers_available = False
try:
    from sentence_transformers import SentenceTransformer
    sentence_transformers_available = True
except ImportError:
    SentenceTransformer = None
    print("⚠️  sentence-transformers 模块不可用，将使用简单检索模式")

# 容错导入 faiss
faiss_available = False
try:
    import faiss
    faiss_available = True
except ImportError:
    faiss = None
    print("⚠️  faiss 模块不可用，将使用简单检索模式")


VECTOR_MODEL = "all-MiniLM-L6-v2"


class VectorSearchEngine:
    """向量检索引擎（支持完整模式和简单模式）"""
    
    def __init__(self):
        self.model = None
        self.index = None
        self.product_texts = []
        self._load_model()
        self._build_index()
    
    def _load_model(self):
        """加载向量模型（如果可用）"""
        if sentence_transformers_available:
            try:
                print("正在加载向量模型:", VECTOR_MODEL, "...")
                self.model = SentenceTransformer(VECTOR_MODEL)
                print("向量模型加载完成")
            except Exception as e:
                print("加载向量模型失败:", e)
                self.model = None
        else:
            print("⚠️  sentence-transformers 不可用，使用简单模式")
    
    def _build_index(self):
        """构建索引（优先完整模式，否则使用简单模式）"""
        try:
            self.product_texts = []
            for p in PRODUCTS:
                text = p["name"] + " " + p["description"] + " 适合温度:" + str(p["min_temp"]) + "-" + str(p["max_temp"]) + "℃ 场合:" + ",".join(p["occasions"])
                self.product_texts.append(text)
            
            if faiss_available and self.model:
                # 完整模式：使用 faiss + sentence-transformers
                embeddings = self.model.encode(self.product_texts, convert_to_numpy=True)
                dimension = embeddings.shape[1]
                
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(embeddings.astype(np.float32))
                print("✅ 向量索引构建完成 (faiss)")
            else:
                print("⚠️  使用简单检索模式")
        except Exception as e:
            print("构建索引失败:", e)
    
    def search(self, query, top_k=3):
        """
        向量相似检索
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            相似商品列表
        """
        try:
            if faiss_available and self.model and self.index:
                # 使用完整向量检索模式
                query_embedding = self.model.encode([query], convert_to_numpy=True).astype(np.float32)
                distances, indices = self.index.search(query_embedding, top_k)
                
                results = []
                for i, idx in enumerate(indices[0]):
                    if idx < len(PRODUCTS):
                        product = PRODUCTS[idx].copy()
                        product["similarity_score"] = float(1.0 / (1.0 + distances[0][i]))
                        results.append(product)
                
                return results
            else:
                # 备用方案：简单关键词匹配
                return self._simple_search(query, top_k)
        except Exception as e:
            print("检索失败:", e)
            return self._simple_search(query, top_k)
    
    def _simple_search(self, query, top_k=3):
        """简单关键词匹配检索（轻量级备用方案）"""
        results = []
        query_lower = query.lower()
        query_words = query_lower.split()
        
        for product in PRODUCTS:
            text = (product["name"] + " " + product["description"] + " " + " ".join(product["occasions"])).lower()
            score = 0.1  # 基础分数
            
            # 完全匹配
            if query_lower in text:
                score += 0.5
            
            # 关键词匹配
            match_count = 0
            for word in query_words:
                if word and word in text:
                    score += 0.2
                    match_count += 1
            
            # 增加一些随机性，让结果更有趣
            import random
            score += random.random() * 0.1
            
            product_copy = product.copy()
            product_copy["similarity_score"] = min(score, 1.0)
            results.append(product_copy)
        
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]


_search_engine = None


def get_vector_engine():
    """获取单例向量检索引擎"""
    global _search_engine
    if _search_engine is None:
        _search_engine = VectorSearchEngine()
    return _search_engine
