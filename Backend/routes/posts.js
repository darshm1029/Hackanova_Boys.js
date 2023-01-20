import express from 'express';
import { createPost, getAllPosts, getPostById, deletePost, likePost, unlikePost,addComment, deleteComment } from '../controllers/post';

const router = express.Router();

router.post('/', createPost);
router.get('/', getAllPosts);
router.get('/:id', getPostById);
router.delete('/:id', deletePost);
router.put('/like/:id', likePost);
router.put('/unlike/:id', unlikePost);
router.post('/comment/:id', addComment);
router.delete('/comment/:id/:comment_id', deleteComment);